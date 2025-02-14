import smtplib
import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List

def send_email(sender_email: str, receiver_emails: List[str], subject: str, template_path: str, app_password: str) -> bool:
    """
    Send email using Gmail SMTP with HTML template to multiple recipients (up to 5)
    """
    try:
        # Validate number of recipients
        if len(receiver_emails) > 5:
            raise ValueError("Maximum 5 recipients allowed")

        # Clean email addresses
        receiver_emails = [email.strip() for email in receiver_emails]
        
        print(f"Reading template from: {template_path}")
        # Read HTML template
        with open(template_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Create MIME message
        msg = MIMEMultipart('alternative')
        msg['From'] = sender_email
        msg['To'] = ', '.join(receiver_emails)
        msg['Subject'] = subject

        # Add HTML content with proper encoding
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)

        # Convert message to string
        email_message = msg.as_string()

        print("Connecting to SMTP server...")
        # Create SMTP session
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            
            # Ensure app_password is str
            if isinstance(app_password, bytes):
                app_password = app_password.decode('utf-8')
            
            print("Attempting login...")
            server.login(str(sender_email), str(app_password))
            
            print("Sending email...")
            # Send email
            server.sendmail(
                from_addr=sender_email,
                to_addrs=receiver_emails,
                msg=email_message
            )
        
        print(f"Email has been sent to: {', '.join(receiver_emails)}")
        return True
        
    except FileNotFoundError:
        print(f"Template file not found: {template_path}")
        return False
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    try:
        # Get inputs from environment variables
        sender_email = os.environ["SENDER_EMAIL"].strip()
        app_password = os.environ["APP_PASSWORD"].strip()
        receiver_emails = [email.strip() for email in os.environ["RECEIVER_EMAILS"].split(',')]
        template_path = os.environ["TEMPLATE_PATH"].strip()
        subject = os.environ.get("SUBJECT", "Email from GitHub Action").strip()
        
        # Debug information
        print(f"Sender: {sender_email}")
        print(f"Recipients: {receiver_emails}")
        print(f"Template: {template_path}")
        print(f"Subject: {subject}")
        
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
        
    except Exception as e:
        print(f"Error in main: {str(e)}")
        import traceback
        print(f"Main Traceback: {traceback.format_exc()}")
        exit(1)
