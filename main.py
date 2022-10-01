import os
import email_service

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

servers = {
    'smtp': 'smtp.yandex.ru',
    'imap': 'imap.yandex.ru',
    'pop3': 'pop.yandex.ru',
}


def get_auth():
    return {
        "login": os.getenv("EMAIL_LOGIN"),
        "password": os.getenv("EMAIL_PASSWORD")
    }


def send_mail():
    message = MIMEMultipart()

    text = input("input text: ")

    message['From'] = os.getenv("SMTP_LOGIN")
    message['Subject'] = input("input subject: ")

    message['To'] = input("input target: ")

    message.attach(MIMEText(text, 'plain'))

    email_service.send(get_auth(), message)

    print("successfully sent email to", message['To'])


if __name__ == '__main__':
    email_service = email_service.EmailService(servers, get_auth())

    print(
        "1. Send mail\n" +
        "2. Receive last message by imap\n" +
        "3. Receive lat message by pop\n"
    )

    choose = int(input())

    if choose == 1:
        send_mail()
    elif choose == 2:
        print(email_service.receive_by_imap())
    elif choose == 3:
        print(email_service.receive_by_pop3(get_auth()))
    else:
        print()
