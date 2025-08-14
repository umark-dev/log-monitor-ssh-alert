import os
import time
from datetime import datetime, timedelta

from utils import load_config, log_message, geoip_lookup, threat_check, block_ip
from alerts import AlertManager
from parser import parse_failed_logins_from_file

config = load_config()
LOG_FILE_PATH = config.get("log_file_path", "/var/log/auth.log")
FAILED_LOGIN_THRESHOLD = config.get("failed_login_threshold", 5)
ALERT_COOLDOWN_MINUTES = config.get("alert_cooldown_minutes", 10)
AUTO_BLOCK = config.get("auto_block_enabled", False)
GEOIP_ENABLED = config.get("geoip_enabled", True)

if not os.path.exists("logs"):
    os.makedirs("logs")

failed_attempts = {}
last_alert_time = None
alert_mgr = AlertManager(config)

def monitor_log():
    global last_alert_time
    log_message("logs/monitor.log", "SSH Intrusion Monitoring Started.")
    print("[*] Monitoring started. Press Ctrl+C to stop.")

    with open(LOG_FILE_PATH, "r") as f:
        f.seek(0, os.SEEK_END)

        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue

            entries = parse_failed_logins_from_file(LOG_FILE_PATH)
            for entry in entries:
                ip = entry.get("ip")
                username = entry.get("username")
                now = datetime.now()

                failed_attempts[ip] = [
                    t for t in failed_attempts.get(ip, []) if now - t < timedelta(minutes=10)
                ]
                failed_attempts[ip].append(now)

                if len(failed_attempts[ip]) >= FAILED_LOGIN_THRESHOLD:
                    if not last_alert_time or (now - last_alert_time).total_seconds() > ALERT_COOLDOWN_MINUTES * 60:
                        geo_info = geoip_lookup(ip) if GEOIP_ENABLED else {}
                        threat_info = threat_check(ip)

                        message = (
                            f"🚨 SSH Intrusion Alert 🚨\n"
                            f"IP: {ip}\n"
                            f"Username: {username}\n"
                            f"Geo: {geo_info.get('country','')} / {geo_info.get('region','')} / {geo_info.get('city','')}\n"
                            f"Threat Score: {threat_info.get('abuse_confidence_score',0)}\n"
                            f"Blacklisted: {threat_info.get('is_blacklisted',False)}"
                        )

                        log_message("logs/monitor.log", f"Intrusion Alert: {ip} | {geo_info} | {threat_info}")
                        alert_mgr.send_alert(f"SSH Intrusion Alert — {ip}", message)

                        if AUTO_BLOCK:
                            if block_ip(ip):
                                log_message("logs/monitor.log", f"IP {ip} automatically blocked.")

                        last_alert_time = now

if __name__ == "__main__":
    try:
        monitor_log()
    except KeyboardInterrupt:
        log_message("logs/monitor.log", "Monitoring stopped by user.")
        print("\n[*] Monitoring stopped.")
