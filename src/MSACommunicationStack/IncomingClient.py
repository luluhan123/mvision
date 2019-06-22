# -*- coding: utf-8 -*-
import io
import os
import socket
import struct
import mmap
import threading
import time


def recvall(sock, count):
    buf = b''
    while count:
        new_buf = sock.recv(count)
        if not new_buf:
            return None
        buf += new_buf
        count -= len(new_buf)
    return buf


class Client:
    def __init__(self, _soc, _addr, _num, _context):
        self.soc = _soc
        self.addr = _addr

        self.context = _context
        self.decimg_list = list()

        self.counter_save = 0
        self.counter_save_rec = 0
        self.counter_save_nor = 0
        self.clientIndex = _num
        self.serFileMsg = None

        self.systemStatus = 'standby'

        self.ready = False
        self.reconstruct_count = 0
        self.navi_count = 0
        self.pos_init = 10000000
        self.pos_count = 0
        self.fileSize = 1560 * 1440 * 2
        self.cpt = 0

        self.receptionTask = threading.Thread(None, self.reception)

    def set_current_state(self, current_state):
        self.systemStatus = current_state

    def enable(self):
        self.systemStatus = 'navi'
        self.receptionTask.start()

    def execute(self):
        if self.systemStatus == 'standby':
            print('system enter into standby')
        elif self.systemStatus == 'navi':
            print('receive_count:', self.cpt)
            image_len = recvall(self.soc, 16)
            if not image_len:
                return
            string_data = recvall(self.soc, int(image_len))
            # self.save_raw(string_data)
            # every time should test whether to save
            #print image_len, ord(string_data[0])*256 + ord(string_data[1])

            self.context.append_new_image(string_data)

            self.cpt += 1

    def reception(self):
        while True:
            # send system status to incoming client
            self.send_order(self.systemStatus)
            self.execute()
            time.sleep(0.1)

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
        # print len(_order), _order
        self.soc.sendall(str(len(_order)).ljust(16))
        self.soc.sendall(_order)
        # print "transmitted...."