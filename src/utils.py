import os
import json
import subprocess
from datetime import datetime
import requests

try:
    import geoip2.database
except ImportError:
    print("[WARN] geoip2 not installed. GeoIP features will not work.")

GEOIP_DB_PATH = "GeoLite2-City.mmdb"  # Download free MaxMind DB

# -------------------
# Configuration Loader
# -------------------
def load_config(config_path="config/config.json") -> dict:
    """
    Load the configuration file for the monitoring tool.
    Returns a dictionary with settings.
    """
    if not os.path.exists(config_path):
        print(f"[ERROR] Config file not found: {config_path}")
        return {}

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"[ERROR] Invalid JSON format in: {config_path}")
        return {}
    except Exception as e:
        print(f"[ERROR] Failed to load config: {e}")
        return {}

# -------------------
# Logging Utilities
# -------------------
def get_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_message(file_path: str, message: str):
    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"[{get_timestamp()}] {message}\n")
    except Exception as e:
        print(f"[ERROR] Failed to write log: {e}")

# -------------------
# GeoIP & Threat Intelligence
# -------------------
def geoip_lookup(ip: str) -> dict:
    info = {"country": "Unknown", "region": "Unknown", "city": "Unknown"}
    if not os.path.exists(GEOIP_DB_PATH):
        return info

    try:
        reader = geoip2.database.Reader(GEOIP_DB_PATH)
        response = reader.city(ip)
        info["country"] = response.country.name
        info["region"] = response.subdivisions.most_specific.name
        info["city"] = response.city.name
        reader.close()
    except Exception:
        pass
    return info

def threat_check(ip: str) -> dict:
    """
    Check IP against AbuseIPDB.
    Replace 'YOUR_API_KEY' with your key or use ENV variable ABUSEIPDB_API_KEY
    """
    result = {"abuse_confidence_score": 0, "is_blacklisted": False}
    API_KEY = os.getenv("ABUSEIPDB_API_KEY", "YOUR_API_KEY")
    url = f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}&maxAgeInDays=90"
    headers = {"Key": API_KEY, "Accept": "application/json"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json().get("data", {})
        score = data.get("abuseConfidenceScore", 0)
        result["abuse_confidence_score"] = score
        result["is_blacklisted"] = score >= 50
    except Exception as e:
        print(f"[WARN] Threat check failed for {ip}: {e}")
    return result

# -------------------
# IP Blocking
# -------------------
def block_ip(ip: str) -> bool:
    """
    Block an IP using iptables.
    """
    try:
        result = subprocess.run(
            ["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"[INFO] IP {ip} blocked successfully.")
            return True
        else:
            print(f"[ERROR] Failed to block IP {ip}: {result.stderr}")
            return False
    except Exception as e:
        print(f"[ERROR] iptables command failed: {e}")
        return False
