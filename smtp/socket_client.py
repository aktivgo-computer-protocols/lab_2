from socket import *
import base64
import time


class SocketSmtpClient:
    def __init__(self, host: str, port: int, auth: []):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.__initialize__(host, port)
        self.__authorize__(auth)

    def __initialize__(self, host: str, port: int):
        self.client_socket.connect((host, port))
        recv = self.client_socket.recv(1024).decode()
        if recv[:3] != '220':
            raise '220 reply not received from server.'

        helo_command = 'EHLO HOST\r\n'
        self.client_socket.send(helo_command.encode())
        recv = self.client_socket.recv(1024).decode()
        if recv[:3] != '250':
            raise '250 reply not received from server.'

    def __authorize__(self, auth: []):
        base64_str = ('\x00' + auth['login'] + "\x00" + auth['password']).encode()
        base64_str = base64.b64encode(base64_str)
        auth_msg = 'AUTH PLAIN '.encode() + base64_str + '\r\n'.encode()
        self.client_socket.send(auth_msg)
        recv = self.client_socket.recv(1024).decode()
        if recv[:3] != '235':
            raise '235 reply not received from server.'

    def send_mail(self, message):
        mail_from = 'MAIL FROM:<%s>\r\n' % message['from']
        self.client_socket.send(mail_from.encode())
        recv = self.client_socket.recv(1024).decode()
        print('After MAIL FROM command: ' + recv)

        rcpt_to = 'RCPT TO:<%s>\r\n' % message['to']
        self.client_socket.send(rcpt_to.encode())
        recv = self.client_socket.recv(1024).decode()
        print('After RCPT TO command: ' + recv)

        data = 'DATA\r\n'
        self.client_socket.send(data.encode())
        recv = self.client_socket.recv(1024).decode()
        print('After DATA command: ' + recv)

        _from = 'From: <%s>\r\n' % message['from']
        self.client_socket.send(_from.encode())

        to = 'To: <%s>\r\n' % message['to']
        self.client_socket.send(to.encode())

        date = time.strftime('Date: %a, %d %b %Y %H:%M:%S +0000\r\n', time.gmtime())
        self.client_socket.send(date.encode())

        subject = "Subject: %s\r\n" % message['subject']
        self.client_socket.send(subject.encode())

        body = message['body'] + '\r\n.\r\n'
        self.client_socket.send(body.encode())

        recv = self.client_socket.recv(1024)
        print('Response after sending message body: ' + recv.decode())

    def close(self):
        q = "QUIT\r\n"
        self.client_socket.send(q.encode())
        self.client_socket.close()
