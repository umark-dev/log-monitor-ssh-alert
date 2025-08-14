import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils import log_message

class AlertManager:
    def __init__(self, config):
        self.config = config
        self.email_cfg = config.get("email", {})
        self.slack_cfg = config.get("slack", {})
        self.sms_cfg = config.get("sms", {})

    def send_email_alert(self, subject, body):
        if not self.email_cfg.get("enabled", False):
            return
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_cfg['sender_email']
            msg['To'] = self.email_cfg['recipient_email']
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(self.email_cfg['smtp_server'], self.email_cfg['smtp_port'])
            if self.email_cfg.get("use_tls", True):
                server.starttls()
            server.login(self.email_cfg['sender_email'], self.email_cfg['sender_password'])
            server.send_message(msg)
            server.quit()

            log_message("logs/monitor.log", f"Email alert sent to {self.email_cfg['recipient_email']}")
        except Exception as e:
            log_message("logs/monitor.log", f"[ERROR] Failed to send email: {e}")

    def send_slack_alert(self, message):
        if not self.slack_cfg.get("enabled", False):
            return
        try:
            webhook_url = self.slack_cfg['webhook_url']
            payload = {"text": message}
            response = requests.post(webhook_url, json=payload, timeout=10)
            if response.status_code == 200:
                log_message("logs/monitor.log", "Slack alert sent successfully")
            else:
                log_message("logs/monitor.log", f"[ERROR] Slack alert failed: {response.text}")
        except Exception as e:
            log_message("logs/monitor.log", f"[ERROR] Slack alert exception: {e}")

    def send_sms_alert(self, message):
        if not self.sms_cfg.get("enabled", False):
            return
        try:
            from twilio.rest import Client
            client = Client(self.sms_cfg['account_sid'], self.sms_cfg['auth_token'])
            client.messages.create(
                body=message,
                from_=self.sms_cfg['from_number'],
                to=self.sms_cfg['to_number']
            )
            log_message("logs/monitor.log", f"SMS alert sent to {self.sms_cfg['to_number']}")
        except Exception as e:
            log_message("logs/monitor.log", f"[ERROR] SMS alert failed: {e}")

    def send_alert(self, subject, message):
        self.send_email_alert(subject, message)
        self.send_slack_alert(message)
        self.send_sms_alert(message)
