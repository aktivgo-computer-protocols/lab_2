import os
import smtplib
import imaplib
import email_service

import email

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

smtp = smtplib.SMTP(host='smtp.yandex.ru')
imap = imaplib.IMAP4_SSL('imap.yandex.ru')

email_service = email_service.EmailService(smtp, imap)


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

    auth = get_auth()

    email_service.send_mail(auth, message)

    print("successfully sent email to", message['To'])


def receive_message_by_imap():
    auth = get_auth()

    print(email.message_from_string(email_service.receive_mail_by_imap(auth)))


if __name__ == '__main__':

    print(
        "1. Send mail\n" +
        "2. Receive last message by imap\n" +
        "3. Receive lat message by pop\n"
    )

    choose = int(input())

    if choose == 1:
        send_mail()
    elif choose == 2:
        receive_message_by_imap()
