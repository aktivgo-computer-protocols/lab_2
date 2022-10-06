import os
import time

from smtp_client import SMTPClient
from imap_client import IMAPClient
from pop3_client import POP3Client
from socket_smtp_client import SocketSmtpClient
from socket_pop3_client import SocketPop3Client

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

HOST = 'mail.fib.kolpkir.ru'


def get_auth():
    return {
        'login': os.getenv('EMAIL_LOGIN'),
        'password': os.getenv('EMAIL_PASSWORD')
    }


def create_smtp_message():
    msg = MIMEMultipart()

    body = input("input body: ")

    msg['From'] = os.getenv("EMAIL_LOGIN")
    msg['Subject'] = input("input subject: ")

    msg["Date"] = time.strftime("%a, %d %b %Y %H:%M:%S %z")

    msg['To'] = input("input target: ")

    msg.attach(MIMEText(body, 'plain'))

    return msg


def create_socket_smtp_message():
    msg = {}

    body = input("input body: ")
    msg['body'] = body

    msg['from'] = os.getenv("EMAIL_LOGIN")
    msg['subject'] = input("input subject: ")
    msg['to'] = input("input target: ")

    return msg


if __name__ == '__main__':
    auth = get_auth()
    smtp = SMTPClient(HOST, auth)
    imap = IMAPClient(HOST, auth)
    pop3 = POP3Client(HOST, auth)
    socket_smtp = SocketSmtpClient(HOST, 25, auth)
    socket_pop3 = SocketPop3Client(HOST, 110, auth)

    while True:
        print(
            '1. Send mail by smtp\n' +
            '2. Receive last message by imap\n' +
            '3. Receive last message by pop\n' +
            '4. Send mail by socket smtp\n' +
            '5. Receive last message by socket pop3\n' +
            '0. Quit\n'
        )

        choose = int(input())

        if choose == 1:
            message = create_smtp_message()
            smtp.send_mail(message)
            print("successfully sent email to", message['To'], '\n')
        elif choose == 2:
            print(imap.receive_last_mail(), '\n')
        elif choose == 3:
            print(pop3.receive_last_mail(), '\n')
        elif choose == 4:
            message = create_socket_smtp_message()
            socket_smtp.send_mail(message)
            print("successfully sent email to", message['to'], '\n')
        elif choose == 5:
            while True:
                print(socket_pop3.list())

                choose = int(input())

                if choose == 0:
                    break

                print(socket_pop3.receive_mail(choose))
        else:
            smtp.close()
            pop3.close()
            socket_smtp.close()
            socket_pop3.close()
            exit()
