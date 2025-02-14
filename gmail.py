import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List

def send_email(sender_email: str, receiver_emails: List[str], subject: str, template_path: str, app_password: str) -> bool:
    """
    Send email using Gmail SMTP with HTML template to multiple recipients (up to 5)
    """
    try:
        if len(receiver_emails) > 5:
            raise ValueError("Maximum 5 recipients allowed")

        receiver_emails = [email.strip() for email in receiver_emails]

        # Read HTML template with explicit encoding
        with open(template_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Debugging: Ensure it's a string
        print(f"Type of html_content: {type(html_content)}")  # Should print <class 'str'>

        # Create MIME message
        msg = MIMEMultipart('alternative')
        msg['From'] = f"GitHub Action <{sender_email}>"
        msg['To'] = ', '.join(receiver_emails)
        msg['Subject'] = subject
        msg['MIME-Version'] = '1.0'

        # ✅ Correct way: Pass as string, not bytes
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, app_password)

            for recipient in receiver_emails:
                try:
                    server.sendmail(sender_email, recipient, msg.as_string())
                    print(f"✅ Email sent successfully to: {recipient}")
                except Exception as e:
                    print(f"❌ Failed to send to {recipient}: {str(e)}")

        return True

    except FileNotFoundError:
        print(f"❌ Template file not found: {template_path}")
        return False
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return False

if __name__ == "__main__":
    sender_email = os.environ["SENDER_EMAIL"].strip()
    app_password = os.environ["APP_PASSWORD"].strip()
    receiver_emails = [email.strip() for email in os.environ["RECEIVER_EMAILS"].split(',')]
    template_path = os.environ["TEMPLATE_PATH"].strip()
    subject = os.environ.get("SUBJECT", "Email from GitHub Action")

    # Ensure all environment variables are strings
    sender_email = str(sender_email)
    app_password = str(app_password)
    subject = str(subject)

    success = send_email(
        sender_email=sender_email,
        receiver_emails=receiver_emails,
        subject=subject,
        template_path=template_path,
        app_password=app_password
    )

    exit(0 if success else 1)
