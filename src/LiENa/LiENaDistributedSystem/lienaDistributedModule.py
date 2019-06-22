#!/usr/bin/python3
# -*- coding: utf-8 -*-
import threading
import time
import socket
from PyQt5.QtCore import QObject, pyqtSignal
from LiENa.LiENaBasic.lienaDefinition import *
from LiENa.LiENaSocket.LienaTcpClient import LienaTcpClient

from LiENa.LiENaRealTimeTask.LienaDecodingTask import LienaDecodingTask
from LiENa.LiENaRealTimeTask.LienaDiagnosisTask import LienaDiagnosisTask
from LiENa.LiENaRealTimeTask.LienaEncodingTask import LienaEncodingTask
from LiENa.LiENaRealTimeTask.LienaHeartbeatTask import LienaHearBeatTask
from LiENa.LiENaRealTimeTask.LienaReceptionTask import LienaReceptionTask
from LiENa.LiENaRealTimeTask.LienaTransmissionTask import LienaTransmissionTask
from LiENa.LiENaRealTimeTask.LienaNTPClockSynchronisationTask import LienaNTPClockSynchronisationTask

from LiENa.LiENaStructure.LiENaDatagramStructure.LienaInputQueue import LienaInputQueue
from LiENa.LiENaStructure.LiENaDatagramStructure.LienaOutputQueue import LienaOutputQueue

from LiENa.LiENaStructure.LiENaMessage.LienaChannelReOpenedMessage import LienaChannelReOpenedMessage
from LiENa.LiENaStructure.LiENaMessage.LienaChannelClosedMessage import LienaChannelClosedMessage
from LiENa.LiENaStructure.LiENaMessage.LienaDisengagementMessage import LienaDisengagementMessage
from LiENa.LiENaStructure.LiENaMessage.LienaHandShakeCommitMessage import LienaHandShakeCommitMessage
from LiENa.LiENaStructure.LiENaMessage.LienaHeartbeatMessage import LienaHeartbeatMessage
from LiENa.LiENaStructure.LiENaMessage.LienaHandShakeMessage import LienaHandShakeMessage
from LiENa.LiENaStructure.LiENaMessage.LienaChannelOpenedMessage import LienaChannelOpenedMessage
from LiENa.LiENaStructure.LiENaMessage.LienaNetworkQualityMessage import LienaNetworkQualityMessage
from LiENa.LiENaStructure.LiENaMessage.LienaReHandshakeCommitMessage import LienaReHandshakeCommitMessage
from LiENa.LiENaStructure.LiENaMessage.lienaReHandshakeMessage import LienaReHandshakeMessage
from LiENa.LiENaStructure.LiENaMessage.LienaDisengagementCommitMessage import LienaDisengagementCommitMessage


class LienaDistributedModule(QObject):
    lostConnexion = pyqtSignal(int)
    restartServer = pyqtSignal()

    def __init__(self, index, global_parameter):
        super(LienaDistributedModule, self).__init__()
        self.global_parameter = global_parameter
        self.index = index

        # -----------------------------------------------------------------------------------
        # common parameter
        # -----------------------------------------------------------------------------------
        self.target_device_id = 0
        self.address = ""
        self.port = self.global_parameter.get_global_port()
        self.open_channel_procedure = 0
        self.connection_status = 0
        self.motivate = False

        # -----------------------------------------------------------------------------------
        # incoming pipeline
        # -----------------------------------------------------------------------------------
        # structure
        self.input_queue = None

        # real time tasks
        self.reception_task = None
        self.decoding_task = None
        self.network_quality_task = None

        # parameter
        self.socket_for_reception = None
        self.reception_task_period = 20
        self.decoding_task_period = 20
        self.reception_task_priority = 1
        self.decoding_task_priority = 1

        # -----------------------------------------------------------------------------------
        # outcome pipeline
        # -----------------------------------------------------------------------------------
        # structure
        self.output_queue = None

        # real time tasks
        self.transmission_task = None
        self.encoding_task = None

        # parameter
        self.socket_for_transmission = None
        self.transmission_task_period = 20
        self.encoding_task_period = 20
        self.transmission_task_priority = 1
        self.encoding_task_priority = 1

        # -----------------------------------------------------------------------------------
        # diagnosis strategy
        # -----------------------------------------------------------------------------------
        # real time tasks
        self.heartbeat_task = None
        self.connexion_diagnosis_task = LienaDiagnosisTask()
        self.connexion_diagnosis_task.lostConnexion.connect(self.launch_recovery_procedure)

        # parameter
        self.heartbeat_task_period = 20
        self.connexion_diagnosis_task_period = 20
        self.heartbeat_task_priority = 1
        self.connexion_diagnosis_task_priority = 1
        self.restartServerNeeded = False
        self.repair_channel_procedure = 0
        self.diagnosis = False
        self.executed = False

    def store_ntp__clock_synchronisation_message(self, msg):
        self.network_quality_task.receive(msg)
        # self.network_quality_task.receive(msg)

    def return_back_network_quality_message(self, msg):
        self.encoding_task.send_back_network_quality_message(msg)

    def heartbeat_message_arrived(self, heartbeat_message):
        if DEBUG:
            print("LienaDistributedModule | heartbeat_message_arrived")
        self.connexion_diagnosis_task.append(heartbeat_message)

        if self.connexion_diagnosis_task.get_sequence_length() == 1:
            if self.motivate:
                if not self.executed:
                    self.network_quality_task = LienaNTPClockSynchronisationTask(self.output_queue, self.global_parameter, self.target_device_id)
                    self.network_quality_task.set_loop_number(10)
                    self.network_quality_task.launch()
                    self.executed = True

    def recovery_task(self):
        print("LienaDistributedModule | recovery_task", self.address, self.port)

        latency = 1
        while True:
            test_connexion = LienaTcpClient(self.address, self.port)
            ret = test_connexion.connectera()
            if ret == LIENA_ERROR_SUCCESS:
                print("success")

                if self.restartServerNeeded:
                    self.restartServer.emit()

                time.sleep(2)

                self.repair_channel_procedure = 1
                self.transmission_task.update_socket_descriptor(test_connexion.get_socket_com())
                self.transmission_task.enable()
                self.encoding_task.enable()
                self.encoding_task.send_rehandshake_message()
                break
            elif ret == LIENA_ERROR_LOCAL_CONNEXION_LOST:
                print("connect your network cable")
                self.restartServerNeeded = True
                latency += 1
            elif ret == LIENA_ERROR_PEER_SERVER_NOT_LAUNCHED:
                print("other side device's software down")
                latency += 1
            elif ret == LIENA_ERROR_PEER_CONNEXION_LOST:
                print("connect other side device's cable")
                latency += 1

            if latency > 8:
                latency = 8

            time.sleep(latency)

    def is_in_diagnosis(self):
        return self.diagnosis

    def launch_recovery_procedure(self):
        self.lostConnexion.emit(self.target_device_id)

        try:
            self.socket_for_transmission.shutdown(2)
        except socket.error as msg_list:
            print(msg_list)

        try:
            self.socket_for_reception.shutdown(2)
        except socket.error as msg_list:
            print(msg_list)

        self.transmission_task.freeze()
        self.reception_task.freeze()
        self.decoding_task.freeze()
        self.encoding_task.freeze()
        self.heartbeat_task.freeze()
        self.input_queue.clear()
        self.output_queue.clear()

        self.diagnosis = True

        if self.motivate:
            threading.Thread(None, self.recovery_task).start()

    def launch_heartbeat_task(self, msg):
        if DEBUG:
            print("LienaDistributedModule | launch_heartbeat_task")
        # msg.get_message_id()& 0xffffffff00000000>>32...
        self.heartbeat_task = LienaHearBeatTask(self.output_queue, self.global_parameter)
        self.heartbeat_task.launch()

    def channel_repaired(self, msg):
        if DEBUG:
            print("LienaDistributedModule | channel_repaired")
        self.encoding_task.send_channel_repaired_message()
        time.sleep(1)
        self.heartbeat_task.enable()
        self.connexion_diagnosis_task.connection_failed_recovery()

    def channel_opened(self, msg):
        if DEBUG:
            print("LienaDistributedModule | channel_open_request")
        self.encoding_task.send_channel_opened_message()
        self.heartbeat_task = LienaHearBeatTask(self.output_queue, self.global_parameter)
        self.heartbeat_task.launch()

    def channel_close_request(self, device_id):
        if DEBUG:
            print("LienaDistributedModule | channel_close_request", device_id)
        self.target_device_id = device_id
        self.encoding_task.send_disengagement_message()

    def launch_module_close_procedure(self, disengagement_commit_message):
        self.heartbeat_task.terminate()
        self.encoding_task.send_channel_closed_message()
        time.sleep(1)
        self.terminate()

    def launch_module_close(self, channel_closed_message):
        self.terminate()

    def launch_disengagement_commit_procedure(self, disengagement_message):
        if DEBUG:
            print("LienaDistributedModule | launch_disengagement_commit_procedure", disengagement_message.get_message_id())
        self.heartbeat_task.terminate()
        self.encoding_task.send_disengagement_commit_message()

    def launch_handshake_commit_procedure(self, handshake_message):

        self.generate_transmission_channel(False, handshake_message.get_ip_address(), handshake_message.get_port())

    def launch_rehandshake_commit_message(self, msg):
        print("LienaDistributedModule | launch_rehandshake_commit_message")
        self.repair_transmission_channel()

    def repair_reception_channel(self, socket_reception):
        if DEBUG:
            print("LienaDistributedModule | repair_reception_channel", self.motivate, self.repair_channel_procedure)
        if self.motivate:
            if self.repair_channel_procedure == 1:
                self.socket_for_reception = socket_reception
                self.reception_task.update_socket_descriptor(self.socket_for_reception)
                self.decoding_task.enable()
                self.reception_task.enable()
        else:
            if self.repair_channel_procedure == 1:
                return
            self.repair_channel_procedure = 1
            self.socket_for_reception = socket_reception
            self.reception_task.update_socket_descriptor(self.socket_for_reception)
            self.decoding_task.enable()
            self.reception_task.enable()

    def build_reception_channel(self):
        print("instantiate an input queue")
        self.input_queue = LienaInputQueue()

        print("instantiate decoding task")
        self.decoding_task = LienaDecodingTask(self.input_queue, self.motivate, self.global_parameter.get_local_device_id(), self.target_device_id)
        self.decoding_task.handshakeMessageArrived[LienaHandShakeMessage].connect(self.launch_handshake_commit_procedure)
        self.decoding_task.channelOpenedMessageArrived[LienaChannelOpenedMessage].connect(self.launch_heartbeat_task)
        self.decoding_task.disengagementMessageArrived[LienaDisengagementMessage].connect(self.launch_disengagement_commit_procedure)
        self.decoding_task.handshakeCommitMessageArrived[LienaHandShakeCommitMessage].connect(self.channel_opened)
        self.decoding_task.disengagementCommitMessageArrived[LienaDisengagementCommitMessage].connect(self.launch_module_close_procedure)
        self.decoding_task.channelClosedMessageArrived[LienaChannelClosedMessage].connect(self.launch_module_close)
        self.decoding_task.heartBeatMessageArrived[LienaHeartbeatMessage].connect(self.heartbeat_message_arrived)
        self.decoding_task.rehandshakeMessageArrived[LienaReHandshakeMessage].connect(self.launch_rehandshake_commit_message)
        self.decoding_task.rehandshakeCommitMessageArrived[LienaReHandshakeCommitMessage].connect(self.channel_repaired)
        self.decoding_task.channelReOpenedMessageArrived[LienaChannelReOpenedMessage].connect(self.launch_channel_reopened)
        self.decoding_task.passiveNTPClockSynchronisationMessageArrived.connect(self.return_back_network_quality_message)
        self.decoding_task.motivateNTPClockSynchronisationMessageArrived.connect(self.store_ntp__clock_synchronisation_message)
        self.decoding_task.launch()

        print("instantiate decoding task")
        self.reception_task = LienaReceptionTask(self.index, self.global_parameter, self.socket_for_reception, self.input_queue, self.target_device_id)
        self.reception_task.launch()

    def generate_reception_channel(self, socket_reception):
        self.socket_for_reception = socket_reception

        if self.motivate:
            if self.open_channel_procedure == 1:
                print("LienaDistributedModule | generate reception channel while motivate procedure")
                self.build_reception_channel()
        else:
            if self.open_channel_procedure == 1:
                return
            self.open_channel_procedure = 1
            print("LienaDistributedModule | generate reception channel while passive procedure")
            self.build_reception_channel()

    def launch_channel_reopened(self, msg):
        if DEBUG:
            print("LienaDistributedModule | launch_channel_reopened")
        self.connexion_diagnosis_task.connection_failed_recovery()
        self.heartbeat_task.enable()

    def repair_transmission_channel(self):
        ret = -1
        if DEBUG:
            print("LienaDistributedModule | repair_transmission_channel", self.motivate, self.open_channel_procedure)
        if self.motivate:
            if self.repair_channel_procedure == 1:
                return ret
            self.repair_channel_procedure = 1

        else:
            if self.open_channel_procedure == 1:
                tcp_client = LienaTcpClient(self.address, self.port)
                ret = tcp_client.connectera()
                if ret == 0:
                    self.encoding_task.enable()
                    self.transmission_task.update_socket_descriptor(tcp_client.get_socket_com())
                    self.transmission_task.enable()
                    self.encoding_task.send_rehandshake_commit_message()

    def generate_transmission_channel(self, motivate, addr, port):
        ret = -1
        self.motivate = motivate
        if DEBUG:
            print("LienaDistributedModule | generate_transmission_channel", motivate, self.open_channel_procedure)
        if motivate:
            if self.open_channel_procedure == 1:
                return ret
            self.open_channel_procedure = 1

            self.address = addr
            self.port = port

            tcp_client = LienaTcpClient(addr, port)
            ret = tcp_client.connectera()

            if ret == 0:
                self.output_queue = LienaOutputQueue()

                self.encoding_task = LienaEncodingTask(self.output_queue, self.global_parameter, self.motivate, self.target_device_id)
                self.encoding_task.launch()

                self.socket_for_transmission = tcp_client.get_socket_com()
                self.transmission_task = LienaTransmissionTask(tcp_client.get_socket_com(), self.index, self.global_parameter, self.output_queue, self.target_device_id)
                self.transmission_task.launch()

                self.encoding_task.send_handshake_message(tcp_client.get_local_ip())

        else:
            if self.open_channel_procedure == 1:
                self.address = addr
                self.port = port

                tcp_client = LienaTcpClient(addr, port)
                ret = tcp_client.connectera()

                if ret == 0:
                    self.output_queue = LienaOutputQueue()

                    self.encoding_task = LienaEncodingTask(self.output_queue, self.global_parameter, self.motivate, self.target_device_id)
                    self.encoding_task.launch()

                    self.transmission_task = LienaTransmissionTask(tcp_client.get_socket_com(), self.index, self.global_parameter, self.output_queue, self.target_device_id)
                    self.socket_for_transmission = tcp_client.get_socket_com()
                    self.transmission_task.launch()

                    self.encoding_task.send_handshake_commit_message()

        return ret

    def set_index(self, index):
        self.index = index

    def set_device_id(self, device_id):
        self.target_device_id = device_id

    def set_address(self, address):
        self.address = address

    def set_port(self, port):
        self.port = port

    def set_socket_for_transmission(self, socket_for_transmission):
        self.socket_for_transmission = socket_for_transmission

    def set_socket_for_reception(self, socket_for_reception):
        self.socket_for_reception = socket_for_reception

    def set_connection_status(self, connection_status):
        self.connection_status = connection_status

    def get_index(self):
        return self.index

    def get_device_id(self):
        return self.target_device_id

    def get_address(self):
        return self.address

    def get_port(self):
        return self.port

    def get_socket_for_reception(self):
        return self.socket_for_reception

    def get_socket_for_transmission(self):
        return self.socket_for_transmission

    def get_connection_status(self):
        return self.connection_status

    def terminate(self):

        try:
            self.socket_for_transmission.shutdown(2)
        except socket.error as msg_list:
            print(msg_list)

        try:
            self.socket_for_reception.shutdown(2)
        except socket.error as msg_list:
            print(msg_list)

        self.heartbeat_task.terminate()
        self.encoding_task.terminate()
        self.decoding_task.terminate()
        self.reception_task.terminate()
        self.transmission_task.terminate()
        self.connexion_diagnosis_task.terminate()
        if DEBUG:
            print("module with", self.target_device_id, "closed")
