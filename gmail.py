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
        # Validate number of recipients
        if len(receiver_emails) > 5:
            raise ValueError("Maximum 5 recipients allowed")

        # Read HTML template
        with open(template_path, 'r') as file:
            html_content = file.read()

        # Create MIME message
        msg = MIMEMultipart('alternative')
        msg['From'] = sender_email
        msg['To'] = ', '.join(receiver_emails)
        msg['Subject'] = subject

        # Add HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)

        # Create SMTP session
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.send_message(msg)
        
        print(f"Email has been sent to: {', '.join(receiver_emails)}")
        return True
        
    except FileNotFoundError:
        print(f"Template file not found: {template_path}")
        return False
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False

def get_valid_email_input() -> str:
    """Get and validate email input from user"""
    while True:
        email = input("Enter email address: ").strip()
        if '@' in email and '.' in email:  # Basic email validation
            return email
        print("Invalid email format. Please try again.")

if __name__ == "__main__":
    # Sender details
    sender_email = "raghulmadhavan1@gmail.com"
    app_password = ""  # Your Gmail App Password here
    
    # Get number of recipients
    while True:
        try:
            num_recipients = int(input("Enter number of recipients (max 5): "))
            if 1 <= num_recipients <= 5:
                break
            print("Please enter a number between 1 and 5")
        except ValueError:
            print("Please enter a valid number")

    # Collect recipient emails
    receiver_emails = []
    print("\nEnter email addresses for recipients:")
    for i in range(num_recipients):
        print(f"\nRecipient {i+1}:")
        email = get_valid_email_input()
        receiver_emails.append(email)
    
    # Email details
    template_path = "templates/email_template.html"
    subject = "Generated mail"
    
    # Confirm before sending
    print("\nReady to send email to:")
    for i, email in enumerate(receiver_emails, 1):
        print(f"{i}. {email}")
    
    confirm = input("\nSend email? (y/n): ").lower()
    if confirm == 'y':
        success = send_email(
            sender_email=sender_email,
            receiver_emails=receiver_emails,
            subject=subject,
            template_path=template_path,
            app_password=app_password
        )
        if success:
            print("\nEmails sent successfully!")
        else:
            print("\nFailed to send emails.")
    else:
        print("\nEmail sending cancelled.")
