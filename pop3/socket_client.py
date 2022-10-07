from socket import *
import base64
import time


class SocketPop3Client:
    def __init__(self, host: str, port: int, auth: []):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.__initialize__(host, port)
        self.__authorize__(auth)

    def __initialize__(self, host: str, port: int):
        self.client_socket.connect((host, port))
        recv = self.client_socket.recv(1024).decode()
        if recv[:3] != '+OK':
            raise '+OK reply not received from server.'

    def __authorize__(self, auth: []):
        user_msg = 'USER %s\r\n' % auth['login']
        self.client_socket.send(user_msg.encode())
        recv = self.client_socket.recv(1024).decode()
        if recv[:3] != '+OK':
            raise '+OK reply not received from server.'

        pass_msg = 'PASS %s\r\n' % auth['password']
        self.client_socket.send(pass_msg.encode())
        recv = self.client_socket.recv(1024).decode()
        if recv[:3] != '+OK':
            raise '+OK reply not received from server.'

    def list(self):
        list_msg = 'LIST\r\n'
        self.client_socket.send(list_msg.encode())
        recv = self.client_socket.recv(1024).decode()
        if recv[:3] != '+OK':
            raise '+OK reply not received from server.'
        return recv

    def receive_mail(self, index: int):
        retr_msg = 'RETR %d\r\n' % index
        self.client_socket.send(retr_msg.encode())
        recv = self.client_socket.recv(1024).decode()
        if recv[:3] != '+OK':
            raise '+OK reply not received from server.'
        return recv

    def close(self):
        q = "QUIT\r\n"
        self.client_socket.send(q.encode())
        self.client_socket.close()
