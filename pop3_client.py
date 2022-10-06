import poplib

from email.parser import BytesParser
from email.policy import default


class POP3Client:
    def __init__(self, host: str, auth: []):
        self.pop3 = poplib.POP3(host)
        self.pop3.user(auth['login'])
        self.pop3.pass_(auth['password'])

    def receive_last_mail(self):
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

    def close(self):
        self.pop3.close()
