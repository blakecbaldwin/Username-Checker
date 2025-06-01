import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

def send_contact_email(name, email, subject, message):
    msg = EmailMessage()
    msg["Subject"] = f"Contact Form: {subject}"
    msg["From"] = os.getenv("SMTP_FROM_EMAIL")
    msg["To"] = os.getenv("SMTP_TO_EMAIL")
    msg.set_content(f"""
You received a new contact form submission:

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}
""")

    try:
        with smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT"))) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(os.getenv("SMTP_USERNAME"), os.getenv("SMTP_PASSWORD"))
            smtp.send_message(msg)
            return True
    except Exception as e:
        print("Failed to send contact email:", e)
        return False
