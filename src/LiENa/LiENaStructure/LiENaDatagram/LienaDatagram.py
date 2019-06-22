from LiENa.LiENaBasic.lienaDefinition import *


class LienaDatagram:
    def __init__(self, size, byte_array):
        self.size = size
        self.byteArray = byte_array
        self.addr = []
        self.port = 0
        self.body = ''
        self.index = 0

    def set_size(self, size):
        self.size = size

    def write_value_in_five_byte(self, start, value):
        self.byteArray[start]     = (value & 0xff00000000) >> 32
        self.byteArray[start + 1] = (value & 0x00ff000000) >> 24
        self.byteArray[start + 2] = (value & 0x0000ff0000) >> 16
        self.byteArray[start + 3] = (value & 0x000000ff00) >> 8
        self.byteArray[start + 4] = (value & 0x00000000ff)

    def get_byte_array(self):
        return self.byteArray

    def get_message_id(self):
        return self.byteArray[0] * (256 ** 7) \
               + self.byteArray[1] * (256 ** 6) \
               + self.byteArray[2] * (256 ** 5) \
               + self.byteArray[3] * (256 ** 4) \
               + self.byteArray[4] * (256 ** 3) \
               + self.byteArray[5] * (256 ** 2) \
               + self.byteArray[6] * 256 \
               + self.byteArray[7]

    def get_origin_id(self):
        return self.byteArray[0] * 256 ** 3 + self.byteArray[1] * 256 ** 2 + self.byteArray[2] * 256 + self.byteArray[3]

    def get_customized_message_id(self):
        return self.byteArray[4] * 256 ** 3 + self.byteArray[5] * 256 ** 2 + self.byteArray[6] * 256 + self.byteArray[7]

    def get_device_class(self):
        return self.get_origin_id() / (32 * 256 ** 3)

    def get_manufacture(self):
        return self.get_origin_id() % (32 * 256 ** 3) / (256 * 2)

    def get_device_type(self):
        return self.get_origin_id() % (256 ** 2) / (256 * 4)

    def get_device_vision(self):
        return self.get_origin_id() % (256 * 4) / 8

    def get_device_index(self):
        return self.get_origin_id() % 8

    def get_target_id(self):
        return self.byteArray[8] * 256 ** 3 + self.byteArray[9] * 256 ** 2 + self.byteArray[10] * 256 + self.byteArray[11]

    def get_time_stamps(self):
        return self.byteArray[12] * 256 ** 4 + self.byteArray[13] * 256 ** 3 + self.byteArray[14] * 256 **2 + self.byteArray[15] * 256 + self.byteArray[16]

    def get_dlc(self):
        return self.byteArray[17] * 256 ** 3 + self.byteArray[18] * 256 ** 2 + self.byteArray[19] * 256 + self.byteArray[20]

    def get_body(self):
        self.body = self.byteArray[HEAD_SIZE:self.size]
        return self.body

    def get_index(self):
        self.index = self.byteArray[19]
        return self.index

    def print_message(self):
        msg = ""
        message_len = len(self.byteArray)
        for i in range(30):
            msg += str(self.byteArray[i]) + "; "
        return msg
