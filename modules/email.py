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
sender_email = "e"
receiver_email = "e"
app_password = "e"  # REPLACE WITH VALID APP PASSWORD
subject = f"Plant Progress Report: {datetime.now().strftime('%m-%d-%Y')}"

# Send email function
def send_email(plant1, plant2, plant3):
    # msg
    body = f"Attached are today’s plant reports by GPT-4o-mini. Every plant has been watered. \n\n\n- Plant 1: {plant1}\n\n- Plant 2: {plant2}\n\n- Plant 3: {plant3}"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    # send
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")