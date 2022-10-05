import imaplib


class IMAPClient:
    def __init__(self, host: str, auth: []):
        self.imap = imaplib.IMAP4(host)
        self.imap.login(auth['login'], auth['password'])

    def receive_last_mail(self):
        self.imap.list()
        self.imap.select("inbox")

        result, data = self.imap.uid('search', "ALL")

        latest_email_uid = data[0].split()[-1]
        result, data = self.imap.uid('fetch', latest_email_uid, '(RFC822)')

        return data[0][1]