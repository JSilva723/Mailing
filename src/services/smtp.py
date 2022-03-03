import os
import smtplib
from email.message import EmailMessage

class SmtpGmail():
    _smtp_email = os.getenv('SMTP_EMAIL')
    _password = os.getenv('SMTP_PASSWORD')
    def __init__(self, to, message, subject):
        self.to = to
        self.message = message
        self.subject = subject

    def send(self):
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(self._smtp_email, self._password)
        msg = EmailMessage()
        msg.add_header('Content-Type','text/html')
        msg.set_payload('{}'.format(self.message))
        server.send_message(msg, self._smtp_email, self.to)
        server.quit()        