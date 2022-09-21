import smtplib
import imaplib


class EmailService:
    smtp: smtplib.SMTP
    imap: imaplib.IMAP4_SSL

    def __init__(self, smtp, imap):
        self.smtp = smtp
        self.imap = imap

    def send_mail(self, auth, message):
        self.smtp.starttls()

        self.smtp.login(auth['login'], auth['password'])

        self.smtp.sendmail(message['From'], message['To'], message.as_string())

        self.smtp.quit()

    def receive_mail_by_imap(self, auth):
        self.imap.login(auth['login'], auth['password'])
        self.imap.list()
        self.imap.select("inbox")

        result, data = self.imap.uid('search', "ALL")

        latest_email_uid = data[0].split()[-1]
        result, data = self.imap.uid('fetch', latest_email_uid, '(RFC822)')

        return data[0][1]
