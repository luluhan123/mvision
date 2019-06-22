# -*- coding: utf-8 -*-
import threading
import time
import socket
from LiENa.LiENaStructure.LiENaDatagram.LienaDatagram import LienaDatagram
from LiENa.LiENaBasic.lienaDefinition import *


class LienaReceptionTask:
    def __init__(self, index, global_parameter, _soc, _input_queue, target_device_id):

        self.index = index
        self.global_parameter = global_parameter
        self.soc = _soc
        self.inputQueue = _input_queue
        self.target_device_id = target_device_id

        self.counter = 0

        self.stand_by = False

        self.serFileMsg = None
        self.systemStatus = 'standby'
        self.ready = False
        self.reconstruct_count = 0
        self.navi_count = 0
        self.pos_init = 10000000
        self.pos_count = 0
        self.fileSize = 1560 * 1440 * 2
        self.datagram_count = 0
        self.rtPeriod = 0.05

        self.flag = True
        self.receptionTask = threading.Thread(None, self.reception)

    def set_real_time_period(self, period):
        self.rtPeriod = period

    def update_socket_descriptor(self, soc):
        self.soc = soc

    def enable(self):
        self.stand_by = False

    def freeze(self):
        self.stand_by = True

    def terminate(self):
        self.flag = False

    def recvall(self, sock, count):
        buf = b''
        while count:
            new_buf = sock.recv(count)
            if not new_buf:
                return None
            buf += new_buf
            count -= len(new_buf)
        return buf

    def set_current_state(self, current_state):
        self.systemStatus = current_state

    def launch(self):
        self.receptionTask.start()

    def reception(self):

        while self.flag:

            if self.stand_by:
                time.sleep(1)
                continue

            try:
                byte_array = self.recvall(self.soc, self.global_parameter.get_global_datagram_size())
            except socket.error as msg:
                if DEBUG:
                    print("receive error", msg[0], msg[1])
                del byte_array
                continue

            if byte_array is not None:
                datagram = LienaDatagram(self.global_parameter.get_global_datagram_size(), bytearray(byte_array))

                if datagram.get_customized_message_id() == LIENA_SESSION_MANAGEMENT_NTP_CLOCK_SYNCHRONIZATION_MESSAGE:
                    if datagram.get_origin_id() == self.global_parameter.get_local_device_id():
                        print("ntp write t4:", int(datagram.get_body()[0]), self.global_parameter.get_current_time_in_microsecond())
                        datagram.write_value_in_five_byte(37, self.global_parameter.get_current_time_in_microsecond())
                    else:
                        print("ntp write t2:", int(datagram.get_body()[0]), self.global_parameter.get_current_time_in_microsecond())
                        datagram.write_value_in_five_byte(27, self.global_parameter.get_current_time_in_microsecond())

                self.inputQueue.append(datagram)
                self.counter += 1

            time.sleep(self.rtPeriod)

    def is_ready(self):
        return self.ready

    def get_id(self):
        return self.clientIndex

    def find_order(self, line):
        line_date = line.translate(None, "\r\n")
        p = line_date.find(':')
        data = line_date[p + 1:len(line_date)]
        return data

    def send_order(self, _order):
        self.soc.sendall(str(len(_order)).ljust(16))
        self.soc.sendall(_order)
        # print "transmitted...."
