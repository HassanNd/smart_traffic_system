import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

def send_traffic_alert_email():
    sender_email =os.getenv("email_sender")
    sender_password =os.getenv("sender_password")
    recipient_email =os.getenv("receip_email")

    msg = EmailMessage()
    msg.set_content("🚦 Traffic jam detected in the monitored zone.")
    msg["Subject"] = "Traffic Jam Alert"
    msg["From"] = sender_email
    msg["To"] = recipient_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        print("✅ Alert email sent!")
    except Exception as e:
        print("❌ Failed to send email:", e)


