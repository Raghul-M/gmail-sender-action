import smtplib
import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List

def send_email(sender_email: str, receiver_emails: List[str], subject: str, template_path: str, app_password: str) -> bool:
    """
    Send email using Gmail SMTP with HTML template to multiple recipients
    """
    try:
        # Debug prints to check input types
        print(f"Type of sender_email: {type(sender_email)}")
        print(f"Type of app_password: {type(app_password)}")
        
        # Clean and validate inputs
        sender_email = str(sender_email).strip()
        app_password = str(app_password).strip()
        receiver_emails = [str(email).strip() for email in receiver_emails]

        # Read template
        with open(template_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = sender_email
        msg['To'] = ', '.join(receiver_emails)
        msg['Subject'] = subject
        
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)

        # Connect to SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()  # Added explicit EHLO
        server.starttls()
        server.ehlo()  # Added second EHLO after TLS
        
        print("Attempting authentication...")
        try:
            # Try direct authentication
            server.login(sender_email, app_password)
        except smtplib.SMTPAuthenticationError as auth_error:
            print(f"Authentication failed: {str(auth_error)}")
            raise
        except Exception as e:
            print(f"Unexpected error during authentication: {str(e)}")
            raise

        # Send email
        server.send_message(msg)
        server.quit()
        
        print(f"Email sent successfully to: {', '.join(receiver_emails)}")
        return True

    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        if 'server' in locals():
            try:
                server.quit()
            except:
                pass
        return False

if __name__ == "__main__":
    try:
        # Get environment variables
        sender_email = os.environ.get("GMAIL_SENDER", "").strip()
        app_password = os.environ.get("GMAIL_APP_PASSWORD", "").strip()
        receiver_emails = [email.strip() for email in os.environ.get("RECIPIENTS", "").split(',')]
        template_path = os.environ.get("TEMPLATE_PATH", "").strip()
        subject = os.environ.get("SUBJECT", "Email from GitHub Action").strip()

        # Validate required inputs
        if not all([sender_email, app_password, receiver_emails, template_path]):
            raise ValueError("Missing required environment variables")

        # Debug info (without sensitive data)
        print("Configuration:")
        print(f"Sender: {sender_email}")
        print(f"Recipients: {receiver_emails}")
        print(f"Template: {template_path}")
        print(f"Subject: {subject}")

        success = send_email(
            sender_email=sender_email,
            receiver_emails=receiver_emails,
            subject=subject,
            template_path=template_path,
            app_password=app_password
        )

        exit(0 if success else 1)

    except Exception as e:
        print(f"Fatal error: {str(e)}")
        import traceback
        print(f"Main traceback: {traceback.format_exc()}")
        exit(1)
