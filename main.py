import os
import time

from smtp_client import SMTPClient
from imap_client import IMAPClient
from pop3_client import POP3Client
from socket_client import SocketClient

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

HOST = 'mail.fib.kolpkir.ru'


def get_auth():
    return {
        'login': os.getenv('EMAIL_LOGIN'),
        'password': os.getenv('EMAIL_PASSWORD')
    }

def create_message():
    message = MIMEMultipart()

    text = input("input text: ")

    message['From'] = os.getenv("EMAIL_LOGIN")
    message['Subject'] = input("input subject: ")

    message["Date"] = time.strftime("%a, %d %b %Y %H:%M:%S %z")

    message['To'] = input("input target: ")

    message.attach(MIMEText(text, 'plain'))

    return message


if __name__ == '__main__':
    while True:
        auth = get_auth()
        smtp = SMTPClient(HOST, auth)
        imap = IMAPClient(HOST, auth)
        pop3 = POP3Client(HOST, auth)
        socket = SocketClient()

        print(
            '1. Send mail\n' +
            '2. Receive last message by imap\n' +
            '3. Receive last message by pop\n' +
            '0. Quit\n'
        )

        choose = int(input())

        if choose == 1:
            message = create_message()
            smtp.send_mail(message)
            print("successfully sent email to", message['To'], '\n')
        elif choose == 2:
            print(imap.receive_last_mail(), '\n')
        elif choose == 3:
            print(pop3.receive_last_mail(), '\n')
        else:
            exit()
