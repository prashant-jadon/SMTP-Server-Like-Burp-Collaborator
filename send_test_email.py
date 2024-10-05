import smtplib
from email.mime.text import MIMEText

# Email content
msg = MIMEText("This is a test email")
msg['Subject'] = "Test Subject"
msg['From'] = "sender@example.com"
msg['To'] = "test@127.0.0.1"

# Send the email to the local SMTP server
with smtplib.SMTP('127.0.0.1', 1025) as server:
    server.sendmail("sender@example.com", ["test@127.0.0.1"], msg.as_string())

print("Test email sent!")
