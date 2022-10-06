import smtplib


class SMTPClient:
    def __init__(self, host: str, auth: []):
        self.smtp = smtplib.SMTP(host)
        self.smtp.login(auth['login'], auth['password'])

    def send_mail(self, message):
        self.smtp.sendmail(message['From'], message['To'], message.as_string())

    def close(self):
        self.smtp.close()
