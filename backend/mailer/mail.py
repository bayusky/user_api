import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import MailerConfig

def mailer(receiver, token, flag) :
    sender_email = MailerConfig.SMTP_USER
    password = MailerConfig.SMTP_PASSWORD
    port = MailerConfig.SMTP_PORT
    print(type(port))
    print(flag)
    
    
    if flag == "register":
        subject = "Verify your email"
        body = f"Please click here to verify http://localhost:3000/verify/{token}"
    else:
        subject = "Reset your password"
        body = f"Please click here to reset password http://localhost:3000/resetpassword/{token}"

    
    if port == "465":
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(MailerConfig.SMTP_RELAY, port, context=context) as server:
            server.login(sender_email, password)
            receiver_email = receiver
            # Create a multipart message and set headers
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject
            # message["Bcc"] = receiver_email  # Recommended for mass emails

            # Add body to email
            message.attach(MIMEText(body, "plain"))

            text = message.as_string()

            # Log in to server using secure context and send email
            # context = ssl.create_default_context()
            server.sendmail(sender_email, receiver_email, text)
    elif port == "587":
        sender_email = MailerConfig.SMTP_USER
        password = MailerConfig.SMTP_PASSWORD
        port = MailerConfig.SMTP_PORT
    
    
        if flag == "register":
            subject = "Verify your email"
            body = f"Please click here to verify http://localhost:3000/verify/{token}"
        else:
            subject = "Reset your password"
            body = f"Please click here to reset password http://localhost:3000/resetpassword/{token}"
    
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(MailerConfig.SMTP_RELAY, port) as server:
            server.starttls(context=context) # Secure the connection with TLS
            server.login(sender_email, password)
            receiver_email = receiver
            # Create a multipart message and set headers
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject
            # message["Bcc"] = receiver_email  # Recommended for mass emails

            # Add body to email
            message.attach(MIMEText(body, "plain"))

            text = message.as_string()

            # Log in to server using secure context and send email
            # context = ssl.create_default_context()
            server.sendmail(sender_email, receiver_email, text)
    else:
        print("Wrong configuration")