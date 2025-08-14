# 🚨 Log Monitoring & SSH Intrusion Alert Tool

**Author:** Muhammad Umar Naheed
**Version:** 2.0.0
**License:** MIT

A **robust and extensible security tool** for **real-time log monitoring** and **SSH intrusion detection** — designed to track suspicious login attempts and alert administrators instantly via **Email, Slack, and SMS**.
Built for **system administrators, DevOps engineers, and security teams** who need **proactive server security**.

---

## 📌 Features

### 🔍 Real-Time Log Monitoring

* Continuous tracking of authentication logs (`/var/log/auth.log` by default).
* Detects **failed SSH login attempts** and **brute-force patterns**.
* Supports **multiple log sources**.

### 📊 Advanced Intrusion Detection

* Dynamic **failed login thresholds** per IP.
* Intelligent **alert cooldown** to prevent spam.
* IP **whitelisting** support to ignore trusted hosts.

### 📡 Multi-Channel Alerts

* **Email Notifications** (SMTP + TLS/SSL supported).
* **Slack Webhook Integration** for team alerts.
* **Optional SMS alerts** via Twilio.
* Alerts include **GeoIP & Threat Intelligence data**.

### 🛡 Security Enhancements

* **GeoIP lookup** identifies attacker location (country, region, city).
* **Automatic IP blocking** via `iptables` or `ufw`.
* **Threat Intelligence Check** via AbuseIPDB API.

### ⚙ Configuration

* JSON-based `config.json` for full customization.
* Environment variables support for sensitive credentials.

### 📈 Logging & Audit Trail

* Detailed monitoring logs stored in `logs/monitor.log`.
* Timestamped entries for audit and forensic purposes.

---

## 📂 Folder Structure

```bash
log-monitor-ssh-alert/
│
├── config/
│   └── config.json        # Configuration for log paths, thresholds, email/Slack/SMS settings
│
├── logs/
│   └── monitor.log        # Log file for monitoring activity
│
├── src/
│   ├── monitor.py         # Main log monitoring script
│   ├── alerts.py          # Email / Slack / SMS alert manager
│   ├── parser.py          # Functions to parse SSH log entries
│   └── utils.py           # Utilities: GeoIP, IP blocking, logging, config loader
│
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── run.sh                 # Shell script to start monitoring
```

---

## ⚡ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/umarx-dev/log-monitoring-tool.git
cd log-monitoring-tool
```

### 2️⃣ Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Download GeoIP Database

Download **GeoLite2-City.mmdb** from MaxMind and place it in the project root.

---

## 🚀 Usage

### 1️⃣ Configure Settings

Edit **`config/config.json`**:

```json
{
  "log_file_path": "/var/log/auth.log",
  "failed_login_threshold": 5,
  "alert_cooldown_minutes": 10,
  "auto_block_enabled": true,
  "geoip_enabled": true,
  "email": { "enabled": true, "smtp_server": "smtp.example.com", "smtp_port": 587, "use_tls": true, "sender_email": "alert@example.com", "sender_password": "your_password", "recipient_email": "admin@example.com" },
  "slack": { "enabled": true, "webhook_url": "https://hooks.slack.com/services/XXXX/YYYY/ZZZZ" },
  "sms": { "enabled": false, "account_sid": "your_twilio_sid", "auth_token": "your_twilio_auth_token", "from_number": "+1234567890", "to_number": "+0987654321" },
  "multi_log_paths": ["/var/log/auth.log", "/var/log/secure"]
}
```

### 2️⃣ Run the Tool

```bash
./run.sh
```

---

## 🛠 Advanced Features

* **GeoIP Integration** – Detect country, region, and city of attacking IPs.
* **IP Auto-Block** – Automatically block malicious IPs via iptables/ufw.
* **Threat Intelligence API** – Check IPs against known blacklists (AbuseIPDB).
* **Multiple Log Sources** – Monitor multiple authentication logs simultaneously.
* **Multi-Channel Alerts** – Email, Slack, and SMS notifications.

---

## 📜 License

This project is licensed under the **MIT License** – free to use, modify, and distribute.

---

**👨‍💻 Developed by:** Muhammad Umar Naheed
**🌐 LinkedIn:** [linkedin.com/in/umarx-dev](https://linkedin.com/in/umarx-dev)
**💻 GitHub:** [github.com/umarx-dev](https://github.com/umarx-dev)