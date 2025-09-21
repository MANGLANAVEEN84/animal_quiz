import smtplib
import ssl
import random
import string
import time
from email.message import EmailMessage

def generate_code(length=6):
    return ''.join(random.choices(string.digits, k=length))

def send_verification_email(receiver_email, code, smtp_server, smtp_port, sender_email, sender_password):
    msg = EmailMessage()
    msg.set_content(f"Your verification code is: {code}")
    msg['Subject'] = 'Your Animal Quiz Verification Code'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)
