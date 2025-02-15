import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List

def send_email(sender_email: str, receiver_emails: List[str], subject: str, template_path: str, app_password: str) -> bool:
    """
    Send email using Gmail SMTP with HTML template to multiple recipients (up to 5).
    """
    try:
        # Validate number of recipients
        if len(receiver_emails) > 5:
            raise ValueError("Maximum 5 recipients allowed")

        # Read HTML template with proper encoding
        with open(template_path, 'r', encoding="utf-8") as file:
            html_content = file.read()

        # Create MIME message
        msg = MIMEMultipart('alternative')
        msg['From'] = sender_email
        msg['To'] = ', '.join(receiver_emails)
        msg['Subject'] = subject

        # Add HTML content safely
        html_part = MIMEText(str(html_content), 'html')
        msg.attach(html_part)

        # Create SMTP session
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.send_message(msg)

        print(f"✅ Email has been sent to: {', '.join(receiver_emails)}")
        return True

    except FileNotFoundError:
        print(f"❌ Template file not found: {template_path}")
        return False
    except Exception as e:
        print(f"❌ Failed to send email: {repr(e)}")  # Debugging with repr()
        return False

if __name__ == "__main__":
    # Get inputs from environment variables
    sender_email = os.environ.get("SENDER_EMAIL")
    app_password = os.environ.get("APP_PASSWORD")
    receiver_emails = os.environ.get("RECEIVER_EMAILS", "").split(',')
    template_path = os.environ.get("TEMPLATE_PATH")
    subject = os.environ.get("SUBJECT", "Email from GitHub Action")

    # Ensure required environment variables are set
    if not sender_email or not app_password or not receiver_emails or not template_path:
        print("❌ Missing required environment variables.")
        exit(1)

    # Send email
    success = send_email(
        sender_email=sender_email,
        receiver_emails=receiver_emails,
        subject=subject,
        template_path=template_path,
        app_password=app_password
    )

    # Set exit code based on success
    exit(0 if success else 1)
