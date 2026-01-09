"""
  RavensPi, 2025-2026
  Module/File: email.py
  Note: An app password from a Google Account is required to send email
"""

# Imports
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
 

# Configuration
sender_email = "johndoesender@example.com"
receiver_email = "johndoe@example.com"  # Send to yourself
app_password = "your_app_specific_password_here"  # Use an app-specific password
subject = f"Plant Progress Report: {datetime.now().strftime('%m-%d-%Y')}"


# Email setup
msg = MIMEText(body)
msg["Subject"] = subject
msg["From"] = sender_email
msg["To"] = receiver_email

# Send email function
def send_email_with_attachments():
    from main import plant1, plant2, plant3  # Import plant reports from main
    body = f"Attached are today’s plant reports by GPT-4o-mini. Every plant has been watered. \n\n- Plant 1: {plant1}\n- Plant 2: {plant2}\n- Plant 3: {plant3}"
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")