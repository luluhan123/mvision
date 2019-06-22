#!/usr/bin/python3
# -*- coding: utf-8 -*-
from LiENa.LiENaBasic.lienaGlobal import LienaGlobal
from LiENa.LiENaDistributedSystem.lienaDistributedSystem import LienaDistributedSystem
from LiENa.LiENaStructure.LiENaMessageStructure.lienaInputMessageCache import LienaInputMessageCache
from LiENa.LiENaStructure.LiENaMessageStructure.lienaOutputMessageCache import LienaOutputMessageCache
from LiENa.LiENaSocket.LienaTcpServer import LienaTcpServer
from PyQt5.QtCore import QObject, pyqtSignal
from LiENa.LiENaBasic.lienaDefinition import *
import time


class Liena(QObject):
    """
          description:
    """
    newHandShakeMsgArrived = pyqtSignal()
    newConnection = pyqtSignal()

    # [0] ---------------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        super(Liena, self).__init__()

        self.system_flag = False

        # the class which contain import parameter of the middleware
        self.globalParameter = LienaGlobal()

        # the global tcp server waiting for motivate incoming distributed module(remote networked device)
        self.tcpServer = LienaTcpServer(self.globalParameter)

        # the class for manage all the real time session ( message exchange, scheduling, failure handling)
        self.distributedSystem = LienaDistributedSystem(self.globalParameter)

        # signals/slots connexion
        self.distributedSystem.needToRestartServer.connect(self.restart_tcp_server)
        self.tcpServer.clientArrived.connect(self.create_reception_channel_by_address)

    # [1] ---------------------------------------------------------------------------------------------------------------------------
    def register_device(self, local_device_id, device_indexes):
        """
            -- declare all distributed modules of a medical robotic distributed system by passing their unique device id

        :param local_device_id:  device id of the local module
        :param device_indexes:   all device id set of a medical robotic
        :return:
        """
        self.globalParameter.set_local_device_id(local_device_id)
        self.distributedSystem.set_robotic_system_module(device_indexes)

    # [2] ---------------------------------------------------------------------------------------------------------------------------
    def launch(self):
        """
            -- launch liena global server wait for motivate incoming distributed module
        :return:
        """
        if not self.system_flag:
            self.tcpServer.launch_server()
            self.system_flag = True

    # [3] ---------------------------------------------------------------------------------------------------------------------------
    def open_session_request(self, target_device_id, target_ip_address, port):
        """
            -- start a real time communication session with the device using target_device_id, target ip address
        :param target_device_id: 
        :param target_ip_address: 
        :param port: 
        :return: 
        """

        # verifier if the global server is launched
        if not self.system_flag:
            self.launch()

        # generate the session and the outgoing pipeline of the session
        self.distributedSystem.create_distributed_module_with_transmission_channel(target_device_id, True, target_ip_address, port)

    # [4] ---------------------------------------------------------------------------------------------------------------------------
    def close_session_request(self, device_id):
        """
            -- close a real time communication session with the device indicated
        :param device_id:
        :return:
        """
        self.distributedSystem.close_session_by_device_id(device_id)

    # [5] ---------------------------------------------------------------------------------------------------------------------------
    def create_reception_channel_by_address(self):
        incoming_socket = self.tcpServer.get_latest_socket()

        if self.distributedSystem.check_module_by_addr(incoming_socket[1]):
            self.distributedSystem.generate_reception_channel_by_addr(incoming_socket[1], incoming_socket[0])
        else:
            self.distributedSystem.create_distributed_module_with_reception_channel(incoming_socket[0])

    # [6] ---------------------------------------------------------------------------------------------------------------------------
    def terminate(self):
        if self.system_flag:
            self.tcpServer.terminate_server()
            self.system_flag = False

    # [7] ---------------------------------------------------------------------------------------------------------------------------
    def restart_tcp_server(self):
        if DEBUG:
            print("close server")
        self.tcpServer.close()
        time.sleep(1)
        if DEBUG:
            print("restart server")
        self.tcpServer.restart()

    def generate_input_cache(self):
        inputMessageCache = LienaInputMessageCache()
        #self.decodingTask.set_input_cache(inputMessageCache)
        return inputMessageCache

    def generate_output_cache(self):
        outputMessageCache = LienaOutputMessageCache()
        #self.encodingTask.set_output_cache(outputMessageCache)
        return outputMessageCache

    def close(self):
        self.context.close_system()
        self.tcpServer.terminate_server()

    # def launch_transmission_task_by_addr(self, addr):
    #     for transmissionTask in self.transmissionTaskManager:
    #         if transmissionTask.get_addr() == addr:
    #             transmissionTask.launch()

    # deprecated
    def create_motivate_module(self, device_id, addr, port):
        self.distributedSystem.create_distributed_module_with_transmission_channel(device_id, True, addr, port)

