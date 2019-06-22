import io
import socket
import threading
from src.MSACommunicationStack.IncomingClient import Client
import os


class TcpServer:
    def __init__(self, context, port):
        self.context = context
        self.port = port
        self.userNum = 0
        self.server_socket = None
        self.flag = True
        self.listeningTask = threading.Thread(None, self.listening)
        self.clientList = list()
        # self.currentDist = ('/home/cheng/Documents/data')
        # self.folderName = "guidewire_sequence"

    # socket use to listenning
    def create_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', self.port))
        self.server_socket.listen(5)
        self.listeningTask.start()

    def terminate_server(self):
        self.flag = False
        self.server_socket.close()

    def listening(self):
        while self.flag:
            print('waiting for the client:', self.userNum)
            connection, address = self.server_socket.accept()
            print('new connection arriving', address)

            client = Client(connection, address, self.userNum, self.context)
            client.launch()

            self.clientList.append(client)

            self.context.open_new_folder()

            self.userNum += 1
            threading._sleep(1)

    def set_current_state(self, current_state):
        for client in self.clientList:
            client.set_current_state(current_state)

    def launch(self):
        self.create_server()

    def close(self):
        self.flag = False