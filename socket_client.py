from socket import *
import base64
import time


class SocketClient:

    def send_mail(self):
        msg = "I love computer networks!\r\n.\r\n"
        mailserver = ("mail.fib.kolpkir.ru", 25)
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect(mailserver)
        recv = clientSocket.recv(1024)
        recv = recv.decode()
        print("Message after connection request:" + recv)
        if recv[:3] != '220':
            print('220 reply not received from server.')
        heloCommand = 'EHLO Vlad\r\n'
        clientSocket.send(heloCommand.encode())
        recv1 = clientSocket.recv(1024)
        recv1 = recv1.decode()
        print("Message after EHLO command:" + recv1)
        if recv1[:3] != '250':
            print('250 reply not received from server.')

        # Info for username and password
        username = "vlad@fib.kolpkir.ru"
        password = "1234"
        base64_str = ("\x00" + username + "\x00" + password).encode()
        base64_str = base64.b64encode(base64_str)
        authMsg = "AUTH PLAIN ".encode() + base64_str + "\r\n".encode()
        clientSocket.send(authMsg)
        recv_auth = clientSocket.recv(1024)
        print(recv_auth.decode())

        mailFrom = "MAIL FROM:<vlad@fib.kolpkir.ru>\r\n"
        clientSocket.send(mailFrom.encode())
        recv2 = clientSocket.recv(1024)
        recv2 = recv2.decode()
        print("After MAIL FROM command: " + recv2)
        rcptTo = "RCPT TO:<vlad@fib.kolpkir.ru>\r\n"
        clientSocket.send(rcptTo.encode())
        recv3 = clientSocket.recv(1024)
        recv3 = recv3.decode()
        print("After RCPT TO command: " + recv3)

        data = "DATA\r\n"
        clientSocket.send(data.encode())
        recv4 = clientSocket.recv(1024)
        recv4 = recv4.decode()
        print("After DATA command: " + recv4)

        from_ = "From: <vlad@fib.kolpkir.ru>\r\n"
        clientSocket.send(from_.encode())

        to_ = "To: <vlad@fib.kolpkir.ru>\r\n"
        clientSocket.send(to_.encode())

        date = time.strftime("Date: %a, %d %b %Y %H:%M:%S +0000\r\n", time.gmtime())
        clientSocket.send(date.encode())

        subject = "Subject: testing my client\r\n"
        clientSocket.send(subject.encode())

        clientSocket.send(msg.encode())

        recv_msg = clientSocket.recv(1024)
        print("Response after sending message body:" + recv_msg.decode())

        quit = "QUIT\r\n"
        clientSocket.send(quit.encode())

        recv5 = clientSocket.recv(1024)
        print(recv5.decode())
        clientSocket.close()
