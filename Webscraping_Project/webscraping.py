import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

password = os.getenv("GMAIL_APP_PASSWORD")
def send(filename):
    from_add = "ayushsingh25nov@gmail.com"
    to_add = "20051202@kiit.ac.in"
    subject = "PYTHON SCRIPT"

    msg = MIMEMultipart()
    msg["From"] = from_add
    msg["To"] = to_add
    msg["Subject"] = subject

    body = "Hey!, Sending message through Python"
    msg.attach(MIMEText(body, "plain"))

    with open(filename, "rb") as my_file:
        part = MIMEBase("application", "octet-stream")
        part.set_payload((my_file).read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", "attachment; filename= " + filename)
    msg.attach(part)

    message = msg.as_string()
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(from_add, password)

    server.sendmail(from_add, to_add, message)

    server.quit()