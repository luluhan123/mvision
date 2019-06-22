# -*- coding: utf-8 -*-
import threading
import time
from LiENa.LiENaBasic.lienaDefinition import *
from LiENa.LiENaStructure.LiENaDatagram.LienaDatagram import LienaDatagram
from LiENa.LiENaStructure.LiENaMessage.LienaNetworkQualityMessage import LienaNetworkQualityMessage


class LienaNTPClockSynchronisationTask:
    def __init__(self, output_queue, global_parameter, target_device_id):
        self.output_queue = output_queue
        self.global_parameter = global_parameter
        self.targetDeviceId = target_device_id

        self.rtPeriod = 0.1
        self.loopNumber = 10

        self.msgReturned = []

        self.flag = None
        self.qos_task = threading.Thread(None, self.qos)

    def qos(self):
        for i in range(self.loopNumber):
            self.send_network_quality_message(i)
            time.sleep(self.rtPeriod)

    def set_loop_number(self, number):
        self.loopNumber = number

    def receive(self, msg):
        self.msgReturned.append(msg)
        if len(self.msgReturned) == self.loopNumber:
            print(" all message returned ")

    def send_network_quality_message(self, count):
        if DEBUG:
            print("LienaNTPSynchronizationTask | send_network_quality_message", count)

        message_id = self.global_parameter.get_local_device_id() * (2 ** 32) + LIENA_SESSION_MANAGEMENT_NTP_CLOCK_SYNCHRONIZATION_MESSAGE
        timestamps = round((time.time() % 86400) * 1000000)
        target_device_id = self.targetDeviceId
        network_quality_message = LienaNetworkQualityMessage(message_id, target_device_id, timestamps, 21)
        network_quality_message.set_index(count)
        network_quality_message.set_t1(0)

        datagram = LienaDatagram(self.global_parameter.get_global_datagram_size(), self.encode_network_quality_message(network_quality_message))
        self.output_queue.append(datagram)

    def encode_network_quality_message(self, message):
        bytes_to_send = bytearray(self.global_parameter.get_global_datagram_size())

        data_type_msb = message.get_message_id() // (2 ** 32)
        data_type_lsb = message.get_message_id() % (2 ** 32)

        bytes_to_send[0] =  (data_type_msb & 0xff000000) >> 24
        bytes_to_send[1] =  (data_type_msb & 0x00ff0000) >> 16
        bytes_to_send[2] =  (data_type_msb & 0x0000ff00) >> 8
        bytes_to_send[3] =  (data_type_msb & 0x000000ff)

        bytes_to_send[4] =  (data_type_lsb & 0xff000000) >> 24
        bytes_to_send[5] =  (data_type_lsb & 0x00ff0000) >> 16
        bytes_to_send[6] =  (data_type_lsb & 0x0000ff00) >> 8
        bytes_to_send[7] =  (data_type_lsb & 0x000000ff)

        bytes_to_send[8] =  (message.get_target_id() & 0xff000000) >> 24
        bytes_to_send[9] =  (message.get_target_id() & 0x00ff0000) >> 16
        bytes_to_send[10] = (message.get_target_id() & 0x0000ff00) >> 8
        bytes_to_send[11] = (message.get_target_id() & 0x000000ff)

        bytes_to_send[12] = (message.get_timestamps() & 0xff00000000) >> 32
        bytes_to_send[13] = (message.get_timestamps() & 0x00ff000000) >> 24
        bytes_to_send[14] = (message.get_timestamps() & 0x0000ff0000) >> 16
        bytes_to_send[15] = (message.get_timestamps() & 0x000000ff00) >> 8
        bytes_to_send[16] = (message.get_timestamps() & 0x00000000ff)

        bytes_to_send[17] = (message.get_dlc() & 0xff000000) >> 24
        bytes_to_send[18] = (message.get_dlc() & 0x00ff0000) >> 16
        bytes_to_send[19] = (message.get_dlc() & 0x0000ff00) >> 8
        bytes_to_send[20] = (message.get_dlc() & 0x000000ff)

        bytes_to_send[21] = message.get_index()

        bytes_to_send[22] = 0  # t1
        bytes_to_send[23] = 0
        bytes_to_send[24] = 0
        bytes_to_send[25] = 0
        bytes_to_send[26] = 0

        bytes_to_send[27] = 0  # t2
        bytes_to_send[28] = 0
        bytes_to_send[29] = 0
        bytes_to_send[30] = 0
        bytes_to_send[31] = 0

        bytes_to_send[32] = 0  # t3
        bytes_to_send[33] = 0
        bytes_to_send[34] = 0
        bytes_to_send[35] = 0
        bytes_to_send[36] = 0

        bytes_to_send[37] = 0  # t4
        bytes_to_send[38] = 0
        bytes_to_send[39] = 0
        bytes_to_send[40] = 0
        bytes_to_send[41] = 0

        for x in range(42, self.global_parameter.get_global_datagram_size()):
            bytes_to_send[x] = 0

        return bytes_to_send

    def launch(self):
        self.flag = True
        self.qos_task.start()

    def terminate(self):
        self.output_queue.clear()
        self.flag = False
