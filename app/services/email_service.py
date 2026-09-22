import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv


load_dotenv()


SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


def send_email(
    recipient: str,
    subject: str,
    body: str,
):
    try:
        if not all([
            SMTP_HOST,
            SMTP_USERNAME,
            SMTP_PASSWORD,
        ]):
            print("Email settings are not configured.")
            return

        message = EmailMessage()
        message["From"] = SMTP_USERNAME
        message["To"] = recipient
        message["Subject"] = subject
        message.set_content(body)

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(message)

        print(f"Email sent successfully to {recipient}")

    except Exception as e:
        print(f"Email sending failed: {e}")