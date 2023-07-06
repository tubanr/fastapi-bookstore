import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(recipient_email: str, subject: str, content: str):
    smtp_server = "smtp.mailtrap.io"
    smtp_password ="e624ce33acdae6"
    smtp_username = "92cd08ad336a37"
    smtp_port = 587


    sender_email= 'tbnrr9193@gmail.com'
    recipient_email='admin@gmail.com'


    message = MIMEMultipart()
    message["From"] = 'tbnrr9193@gmail.com'
    message["To"]= recipient_email
    message["Subject"]= subject
    #email content
    message.attach(MIMEText(content, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email,  recipient_email, message.as_string())




