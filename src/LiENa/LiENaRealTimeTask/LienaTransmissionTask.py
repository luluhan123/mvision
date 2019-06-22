# -*- coding: utf-8 -*-
import socket
import threading
import time
import os
import sys

from LiENa.LiENaStructure.LiENaDatagram.LienaEncoder import LienaEncoder
from LiENa.LiENaStructure.LiENaDatagramStructure.LienaOutputQueue import LienaOutputQueue
from LiENa.LiENaStructure.LiENaMessage.LienaHandShakeMessage import LienaHandShakeMessage
from LiENa.LiENaStructure.LiENaMessage.LienaHandShakeCommitMessage import LienaHandShakeCommitMessage

from LiENa.LiENaBasic.lienaDefinition import *


class LienaTransmissionTask:
    def __init__(self, socket_transmission, index, global_parameter, output_queue, target_device_id):
        self.launching = False

        self.index = index
        self.global_parameter = global_parameter
        self.socket_transmission = socket_transmission
        self.outputQueue = output_queue
        self.target_device_id = target_device_id
        self.counter = 0

        self.stand_by = False
        self.rtPeriod = 0.05

        self.transmissionTask = threading.Thread(None, self.execute_rt_task)

    def set_real_time_period(self, period):
        self.rtPeriod = period

    def enable(self):
        self.stand_by = False

    def freeze(self):
        self.stand_by = True

    def terminate(self):
        self.launching = False

    def launch(self):
        self.launching = True
        self.transmissionTask.start()

    def update_socket_descriptor(self, soc):
        self.socket_transmission = soc

    def do_transmit(self):
        if self.outputQueue.get_length() > 0:
            datagram = self.outputQueue.get_front_array()
            print("lienaTransmissionTask", datagram.get_origin_id())

            if datagram is None:
                return

            if datagram.get_customized_message_id() == LIENA_SESSION_MANAGEMENT_NTP_CLOCK_SYNCHRONIZATION_MESSAGE:

                if datagram.get_origin_id() == self.global_parameter.get_local_device_id():
                    print("ntp write t1:", int(datagram.get_body()[0]), self.global_parameter.get_current_time_in_microsecond())
                    datagram.write_value_in_five_byte(22, self.global_parameter.get_current_time_in_microsecond())
                else:
                    print("ntp write t3:", int(datagram.get_body()[0]), self.global_parameter.get_current_time_in_microsecond())
                    datagram.write_value_in_five_byte(32, self.global_parameter.get_current_time_in_microsecond())

            try:
                self.socket_transmission.sendall(datagram.get_byte_array())
                if DEBUG:
                    print(self.counter, "LienaTransmissionTask | transmitting ", datagram.get_customized_message_id())
                self.counter += 1
                del datagram
                sys.stdout.flush()

            except socket.error as msg:
                if DEBUG:
                    print("failed", msg, self.counter, "LienaTransmissionTask | transmitting", datagram.print_message())
                sys.stdout.flush()
                del datagram
                return

    def execute_rt_task(self):
        while self.launching:

            if self.stand_by:
                time.sleep(1)
                continue

            self.do_transmit()
            time.sleep(self.rtPeriod)

    def generate_msg(self, v):
        # header 10 byte
        data_type = 8  # 2
        origin_id = 0  # 1
        target_id = 0  # 1
        timestamps = 123456  # 4
        dlc = 4  # 2

        # body
        motor_type = 0  # 1
        symbol = 0  # 1
        speed = 120  # 2

        timestamps_msb = timestamps / (2 ** 16)
        timestamps_lsb = timestamps % (2 ** 16)

        value = int(v)

        if value > 255:
            value = 255
        if value < 0:
            value = 0

        msg = chr(data_type % 256) + chr(data_type / 256) \
              + chr(origin_id) + chr(target_id) \
              + chr(timestamps_lsb % 256) + chr(timestamps_lsb / 256) \
              + chr(timestamps_msb % 256) + chr(timestamps_msb / 256) \
              + chr(dlc % 256) + chr(dlc / 256) + chr(value)
        msg_len = len(msg)
        for x in range(msg_len, 1024):
            msg += ' '

        self.cpt += 1

        return msg

    def new_send_handshake_message(self):
        message_id = SIEMENS_CBCT_ARCADIS_ORBIC_VERSION_1*(2**32) + LIENA_SESSION_MANAGEMENT_HANDSHAKE_MESSAGE

        handshake_message = LienaHandShakeMessage(message_id, 0, 123456, 6, [192, 168, 1, 102], 10704)
        if DEBUG:
            print("LienaTransmissionTask | new_send_handshake_message", message_id)

        encoder = LienaEncoder(self.global_parameter)
        datagram = encoder.encode(handshake_message)

        if datagram is not None:
            self.socket_transmission.sendall(datagram.get_byte_array())

    def launch_trasmission_task(self):
        if DEBUG:
            print("LienaTransmissionTask | connected... start real time communication task")
        self.launching = True
        self.transmissionTask.start()

    def fermeture(self):
        self.connection.close()

    def task(self):
        if len(self.msg_list) > 0:
            self.connection.sendall(self.msg_list.pop(0))

    def read_all(self, count):
        buf = b''
        while count:
            receiving_buffer = self.clientSocket.recv(count)
            if not receiving_buffer:
                return None
            buf += receiving_buffer
            count -= len(receiving_buffer)
        return buf

    def transmit(self, file_path):

        if os.path.exists(file_path):
            img = self.do_parse_raw_file(file_path)
            self.connection.sendall(str(len(img)).ljust(16))
            self.connection.sendall(img)
            # time.sleep(0.02)
            os.remove(file_path)
            if DEBUG:
                print(file_path, "LienaTransmissionTask | transmitted")
            return True
        else:
            img = self.do_parse_raw_file('./navi/default.raw')
            self.connection.sendall(str(len(img)).ljust(16))
            self.connection.sendall(img)
            # print "waiting for", image_a_envoye
            time.sleep(1)
            return False

    def do_parse_raw_file(self, path):
        f = open(path, "r+b")
        img = f.read()
        f.close()
        return img

    def status_check(self):
        type_len = self.read_all(16)

        if not type_len:
            if DEBUG:
                print("error,unknow type file")

        self.system_status = self.read_all(int(type_len))
        # print "system status:", self.system_status

    # def get_addr(self):
    #     return self.addr
