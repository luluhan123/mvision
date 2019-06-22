from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import socket
import threading

from LiENa.LiENaSocket.LienaTcpClient import LienaTcpClient


class LienaTcpServer(QObject):
    localIpDetect = pyqtSignal()
    clientArrived = pyqtSignal()

    def __init__(self, global_parameter):
        super(LienaTcpServer, self).__init__()
        self.globalParameter = global_parameter

        self.port = 10704
        self.userNum = 0
        self.server_socket = None
        self.flag = True
        self.clientList = list()

    def restart(self):
        # stop previous server
        self.flag = True

        # self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server_socket.bind(('0.0.0.0', self.port))
        # self.server_socket.listen(5)
        threading.Thread(None, self.listening).start()

    # socket use to listening
    def launch_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', self.port))
        self.server_socket.listen(5)
        threading.Thread(None, self.listening).start()

    def terminate_server(self):
        print("socket server close")
        self.flag = False
        if self.server_socket is not None:
            self.server_socket.close()

    def listening(self):
        while self.flag:
            print("waiting ...")
            connection, address = self.server_socket.accept()
            print('incoming connection...', address)
            if address[0] == "127.0.0.1":
                break

            # connection.setblocking(0)
            # bsize = connection.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
            # print("passive Buffer size [Before]: %d" % bsize)
            # connection.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            # connection.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10)
            # connection.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 13176 * 2)
            # bsize = connection.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
            # print("passive Buffer size [After] : %d" % bsize)

            self.clientList.append((connection, address[0]))
            self.clientArrived.emit()
            self.userNum += 1
        print("out of listening task")

    def get_latest_socket(self):
        return self.clientList.pop(-1)

    def launch(self):
        self.launch_server()

    def close(self):
        self.flag = False
        close_request = LienaTcpClient("127.0.0.1", self.port)
        close_request.connectera()
