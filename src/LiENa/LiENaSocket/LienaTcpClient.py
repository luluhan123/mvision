import socket
from PyQt5.QtCore import QObject
from LiENa.LiENaBasic.lienaDefinition import *


class LienaTcpClient(QObject):

    def __init__(self, addr, port):
        super(LienaTcpClient, self).__init__()
        self.addr = addr
        self.port = port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.settimeout(2)

    def connectera(self):
        ret = -1
        try:
            print("try connect to target device:", self.addr, self.port)
            self.connection.connect((self.addr, self.port))
            ret = LIENA_ERROR_SUCCESS
        except socket.error as msg:
            if msg == "timed out":
                ret = LIENA_ERROR_PEER_CONNEXION_LOST
            elif msg == "Network is unreachable":
                ret = LIENA_ERROR_LOCAL_CONNEXION_LOST
            elif msg == "connection refused":
                ret = LIENA_ERROR_PEER_SERVER_NOT_LAUNCHED

        # self.connection.setblocking(0)
        # send_buffer_size = self.connection.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
        # receive_buffer_size = self.connection.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
        # print("motivate Buffer size [Before]:", send_buffer_size, receive_buffer_size)

        # self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        # self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 13176*2)
        # self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 10)
        # bsize = self.connection.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
        # print("motivate Buffer size [After] : %d" % bsize)

        return ret

    def get_socket_com(self):
        return self.connection

    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip
