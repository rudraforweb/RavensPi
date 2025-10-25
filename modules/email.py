# --- CONFIGURATION ---
sender_email = "johndoesender@example.com"
receiver_email = "johndoe@example.com"  # Send to yourself
app_password = "your_app_specific_password_here"  # Use an app-specific password
subject = f"Plant Progress Report: {datetime.now().strftime('%m-%d-%Y')}"
body = "Attached are today’s plant images with AI-generated status reports.\n\n- Plant 1: Needs water\n- Plant 2: Healthy\n- Plant 3: Possible overwatering"


# --- EMAIL SETUP ---
msg = MIMEText(body)
msg["Subject"] = subject
msg["From"] = sender_email
msg["To"] = receiver_email

def send_email_with_attachments():
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")