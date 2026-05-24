import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

REQUIRED_SMTP_ENV_VARS = [
    "SMTP_SERVER",
    "SMTP_PORT",
    "SMTP_USERNAME",
    "SMTP_PASSWORD",
    "SMTP_FROM_EMAIL",
    "SMTP_TO_EMAIL",
]


def _smtp_config():
    config = {name: os.getenv(name) for name in REQUIRED_SMTP_ENV_VARS}
    missing = [name for name, value in config.items() if not value]
    if missing:
        print("Contact email blocked: missing SMTP configuration")
        return None
    return config


def send_contact_email(name, email, subject, message):
    config = _smtp_config()
    if not config:
        return False

    msg = EmailMessage()
    msg["Subject"] = f"Contact Form: {subject}"
    msg["From"] = config["SMTP_FROM_EMAIL"]
    msg["To"] = config["SMTP_TO_EMAIL"]
    msg.set_content(f"""
You received a new contact form submission:

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}
""")

    try:
        with smtplib.SMTP(config["SMTP_SERVER"], int(config["SMTP_PORT"]), timeout=10) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(config["SMTP_USERNAME"], config["SMTP_PASSWORD"])
            smtp.send_message(msg)
            return True
    except Exception as e:
        print(f"Failed to send contact email: {e.__class__.__name__}")
        return False
