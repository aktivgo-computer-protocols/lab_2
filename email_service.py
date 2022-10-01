import smtplib
import imaplib
import poplib

from email.parser import BytesParser
from email.policy import default


class EmailService:
    def __init__(self, servers: dict, auth: []):
        self.smtp = smtplib.SMTP(host=servers['smtp'])

        self.imap = imaplib.IMAP4_SSL(servers['imap'])
        self.imap.login(auth['login'], auth['password'])

        self.pop3 = poplib.POP3(servers['pop3'])

    def send(self, auth, message):
        self.smtp.starttls()
        self.smtp.login(auth['login'], auth['password'])
        self.smtp.sendmail(message['From'], message['To'], message.as_string())
        self.smtp.quit()

    def receive_by_imap(self):
        self.imap.list()
        self.imap.select("inbox")

        result, data = self.imap.uid('search', "ALL")

        latest_email_uid = data[0].split()[-1]
        result, data = self.imap.uid('fetch', latest_email_uid, '(RFC822)')

        return data[0][1]

    def receive_by_pop3(self, auth):
        self.pop3.user(auth['login'])
        self.pop3.pass_(auth['password'])

        print(self.pop3.getwelcome())

        stat = self.pop3.stat()
        print(stat)

        l = self.pop3.list()
        print(l)

        r = self.pop3.retr(len(l[1]))
        print(r, len(l[1]))

        bp = BytesParser(policy=default).parsebytes(b'\r\n'.join(r[1]))
        print(type(bp))

        for part in bp.walk():
            print(part.get_content_type())
            if part.get_content_maintype() == 'text':
                return part.get_content()
