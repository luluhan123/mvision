from LiENa.LiENaStructure.LiENaDatagram.LienaDatagram import LienaDatagram
from LiENa.LiENaBasic.lienaDefinition import *


class LienaEncoder:
    def __init__(self, global_parameter):
        self.global_parameter = global_parameter
        self.messageID = 0

    def encode(self, message):
        datagram = None

        self.messageID = message.get_message_id()
        message_type = self.messageID % (2 ** 32)

        if message_type == LIENA_SESSION_MANAGEMENT_HANDSHAKE_MESSAGE:
            datagram = LienaDatagram(self.global_parameter.get_global_datagram_size(), self.encode_handshake_message(message))
        elif message_type == LIENA_SESSION_MANAGEMENT_CHANNEL_OPENED_MESSAGE:
            datagram = LienaDatagram(self.global_parameter.get_global_datagram_size(), self.encode_channelopened_message(message))
        elif message_type == LIENA_SESSION_MANAGEMENT_HEARTBEAT_MESSAGE:
            datagram = LienaDatagram(self.global_parameter.get_global_datagram_size(), self.encode_heartbeat_message(message))
        elif message_type == LIENA_SESSION_MANAGEMENT_HANDSHAKE_COMMIT_MESSAGE:
            datagram = LienaDatagram(self.global_parameter.get_global_datagram_size(), self.encode_handshake_commit_message(message))
        elif message_type == LIENA_SESSION_MANAGEMENT_DISENGAGEMENT_MESSAGE:
            datagram = LienaDatagram(self.global_parameter.get_global_datagram_size(), self.encode_disengagement_message(message))
        elif message_type == LIENA_SESSION_MANAGEMENT_DISENGAGEMENTCOMMIT_MESSAGE:
            datagram = LienaDatagram(self.global_parameter.get_global_datagram_size(), self.encode_disengagement_commit_message(message))
        elif message_type == LIENA_SESSION_MANAGEMENT_CHANNEL_CLOSED_MESSAGE:
            datagram = LienaDatagram(self.global_parameter.get_global_datagram_size(), self.encode_channel_closed_message(message))
        elif message_type == LIENA_SESSION_MANAGEMENT_REHANDSHAKE_MESSAGE:
            datagram = LienaDatagram(self.global_parameter.get_global_datagram_size(), self.encode_rehandshake_message(message))
        elif message_type == LIENA_SESSION_MANAGEMENT_REHANDSHAKECOMMIT_MESSAGE:
            datagram = LienaDatagram(self.global_parameter.get_global_datagram_size(), self.encode_rehandshake_commit_message(message))
        elif message_type == LIENA_SESSION_MANAGEMENT_CHANNEL_REOPENED_MESSAGE:
            datagram = LienaDatagram(self.global_parameter.get_global_datagram_size(), self.encode_channel_reopened_message(message))
        elif message_type == LIENA_SESSION_MANAGEMENT_NTP_CLOCK_SYNCHRONIZATION_MESSAGE:
            datagram = LienaDatagram(self.global_parameter.get_global_datagram_size(), self.encode_network_quality_message(message))

        return datagram

    def encode_network_quality_message(self, message):
        bytes_to_send = bytearray(self.global_parameter.get_global_datagram_size())

        data_type_msb = message.get_message_id() // (2 ** 32)
        data_type_lsb = message.get_message_id() % (2 ** 32)

        bytes_to_send[0] = (data_type_msb & 0xff000000) >> 24
        bytes_to_send[1] = (data_type_msb & 0x00ff0000) >> 16
        bytes_to_send[2] = (data_type_msb & 0x0000ff00) >> 8
        bytes_to_send[3] = (data_type_msb & 0x000000ff)

        bytes_to_send[4] = (data_type_lsb & 0xff000000) >> 24
        bytes_to_send[5] = (data_type_lsb & 0x00ff0000) >> 16
        bytes_to_send[6] = (data_type_lsb & 0x0000ff00) >> 8
        bytes_to_send[7] = (data_type_lsb & 0x000000ff)

        bytes_to_send[8] = (message.get_target_id() & 0xff000000) >> 24
        bytes_to_send[9] = (message.get_target_id() & 0x00ff0000) >> 16
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

        bytes_to_send[22] = (message.get_t1() & 0xff00000000) >> 32
        bytes_to_send[23] = (message.get_t1() & 0x00ff000000) >> 24
        bytes_to_send[24] = (message.get_t1() & 0x0000ff0000) >> 16
        bytes_to_send[25] = (message.get_t1() & 0x000000ff00) >> 8
        bytes_to_send[26] = (message.get_t1() & 0x00000000ff)

        bytes_to_send[27] = (message.get_t2() & 0xff00000000) >> 32  # t2
        bytes_to_send[28] = (message.get_t2() & 0x00ff000000) >> 24
        bytes_to_send[29] = (message.get_t2() & 0x0000ff0000) >> 16
        bytes_to_send[30] = (message.get_t2() & 0x000000ff00) >> 8
        bytes_to_send[31] = (message.get_t2() & 0x00000000ff)

        bytes_to_send[32] = (message.get_t3() & 0xff00000000) >> 32  # t3
        bytes_to_send[33] = (message.get_t3() & 0x00ff000000) >> 24
        bytes_to_send[34] = (message.get_t3() & 0x0000ff0000) >> 16
        bytes_to_send[35] = (message.get_t3() & 0x000000ff00) >> 8
        bytes_to_send[36] = (message.get_t3() & 0x00000000ff)

        bytes_to_send[37] = (message.get_t4() & 0xff400000000) >> 32  # t4
        bytes_to_send[38] = (message.get_t4() & 0x00ff000000) >> 24
        bytes_to_send[39] = (message.get_t4() & 0x0000ff0000) >> 16
        bytes_to_send[40] = (message.get_t4() & 0x000000ff00) >> 8
        bytes_to_send[41] = (message.get_t4() & 0x00000000ff)

        for x in range(42, self.global_parameter.get_global_datagram_size()):
            bytes_to_send[x] = 0

        return bytes_to_send

    def encode_channel_reopened_message(self, message):
        bytes_to_send = bytearray(self.global_parameter.get_global_datagram_size())

        data_type_msb = message.get_message_id() // (2 ** 32)
        data_type_lsb = message.get_message_id() % (2 ** 32)

        bytes_to_send[0] = (data_type_msb & 0xff000000) >> 24
        bytes_to_send[1] = (data_type_msb & 0x00ff0000) >> 16
        bytes_to_send[2] = (data_type_msb & 0x0000ff00) >> 8
        bytes_to_send[3] = (data_type_msb & 0x000000ff)
        bytes_to_send[4] = (data_type_lsb & 0xff000000) >> 24
        bytes_to_send[5] = (data_type_lsb & 0x00ff0000) >> 16
        bytes_to_send[6] = (data_type_lsb & 0x0000ff00) >> 8
        bytes_to_send[7] = (data_type_lsb & 0x000000ff)
        bytes_to_send[8] = (message.get_target_id() & 0xff000000) >> 24
        bytes_to_send[9] = (message.get_target_id() & 0x00ff0000) >> 16
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

        for x in range(21, self.global_parameter.get_global_datagram_size()):
            bytes_to_send[x] = 0

        return bytes_to_send

    def encode_rehandshake_commit_message(self, message):
        bytes_to_send = bytearray(self.global_parameter.get_global_datagram_size())

        data_type_msb = message.get_message_id() // (2 ** 32)
        data_type_lsb = message.get_message_id() % (2 ** 32)

        bytes_to_send[0] = (data_type_msb & 0xff000000) >> 24
        bytes_to_send[1] = (data_type_msb & 0x00ff0000) >> 16
        bytes_to_send[2] = (data_type_msb & 0x0000ff00) >> 8
        bytes_to_send[3] = (data_type_msb & 0x000000ff)
        bytes_to_send[4] = (data_type_lsb & 0xff000000) >> 24
        bytes_to_send[5] = (data_type_lsb & 0x00ff0000) >> 16
        bytes_to_send[6] = (data_type_lsb & 0x0000ff00) >> 8
        bytes_to_send[7] = (data_type_lsb & 0x000000ff)
        bytes_to_send[8] = (message.get_target_id() & 0xff000000) >> 24
        bytes_to_send[9] = (message.get_target_id() & 0x00ff0000) >> 16
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

        for x in range(21, self.global_parameter.get_global_datagram_size()):
            bytes_to_send[x] = 0

        return bytes_to_send

    def encode_rehandshake_message(self, message):
        bytes_to_send = bytearray(self.global_parameter.get_global_datagram_size())

        data_type_msb = message.get_message_id() // (2 ** 32)
        data_type_lsb = message.get_message_id() % (2 ** 32)

        bytes_to_send[0] = (data_type_msb & 0xff000000) >> 24
        bytes_to_send[1] = (data_type_msb & 0x00ff0000) >> 16
        bytes_to_send[2] = (data_type_msb & 0x0000ff00) >> 8
        bytes_to_send[3] = (data_type_msb & 0x000000ff)
        bytes_to_send[4] = (data_type_lsb & 0xff000000) >> 24
        bytes_to_send[5] = (data_type_lsb & 0x00ff0000) >> 16
        bytes_to_send[6] = (data_type_lsb & 0x0000ff00) >> 8
        bytes_to_send[7] = (data_type_lsb & 0x000000ff)
        bytes_to_send[8] = (message.get_target_id() & 0xff000000) >> 24
        bytes_to_send[9] = (message.get_target_id() & 0x00ff0000) >> 16
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

        for x in range(21, self.global_parameter.get_global_datagram_size()):
            bytes_to_send[x] = 0

        return bytes_to_send

    def encode_channel_closed_message(self, message):
        bytes_to_send = bytearray(self.global_parameter.get_global_datagram_size())

        data_type_msb = message.get_message_id() // (2 ** 32)
        data_type_lsb = message.get_message_id() % (2 ** 32)

        bytes_to_send[0] = (data_type_msb & 0xff000000) >> 24
        bytes_to_send[1] = (data_type_msb & 0x00ff0000) >> 16
        bytes_to_send[2] = (data_type_msb & 0x0000ff00) >> 8
        bytes_to_send[3] = (data_type_msb & 0x000000ff)
        bytes_to_send[4] = (data_type_lsb & 0xff000000) >> 24
        bytes_to_send[5] = (data_type_lsb & 0x00ff0000) >> 16
        bytes_to_send[6] = (data_type_lsb & 0x0000ff00) >> 8
        bytes_to_send[7] = (data_type_lsb & 0x000000ff)
        bytes_to_send[8] = (message.get_target_id() & 0xff000000) >> 24
        bytes_to_send[9] = (message.get_target_id() & 0x00ff0000) >> 16
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

        for x in range(21, self.global_parameter.get_global_datagram_size()):
            bytes_to_send[x] = 0

        return bytes_to_send

    def encode_disengagement_commit_message(self, message):
        bytes_to_send = bytearray(self.global_parameter.get_global_datagram_size())

        data_type_msb = message.get_message_id() // (2 ** 32)
        data_type_lsb = message.get_message_id() % (2 ** 32)

        bytes_to_send[0] = (data_type_msb & 0xff000000) >> 24
        bytes_to_send[1] = (data_type_msb & 0x00ff0000) >> 16
        bytes_to_send[2] = (data_type_msb & 0x0000ff00) >> 8
        bytes_to_send[3] = (data_type_msb & 0x000000ff)
        bytes_to_send[4] = (data_type_lsb & 0xff000000) >> 24
        bytes_to_send[5] = (data_type_lsb & 0x00ff0000) >> 16
        bytes_to_send[6] = (data_type_lsb & 0x0000ff00) >> 8
        bytes_to_send[7] = (data_type_lsb & 0x000000ff)
        bytes_to_send[8] = (message.get_target_id() & 0xff000000) >> 24
        bytes_to_send[9] = (message.get_target_id() & 0x00ff0000) >> 16
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

        for x in range(21, self.global_parameter.get_global_datagram_size()):
            bytes_to_send[x] = 0

        return bytes_to_send

    def encode_disengagement_message(self, message):
        bytes_to_send = bytearray(self.global_parameter.get_global_datagram_size())

        data_type_msb = message.get_message_id() // (2 ** 32)
        data_type_lsb = message.get_message_id() % (2 ** 32)

        bytes_to_send[0] = (data_type_msb & 0xff000000) >> 24
        bytes_to_send[1] = (data_type_msb & 0x00ff0000) >> 16
        bytes_to_send[2] = (data_type_msb & 0x0000ff00) >> 8
        bytes_to_send[3] = (data_type_msb & 0x000000ff)
        bytes_to_send[4] = (data_type_lsb & 0xff000000) >> 24
        bytes_to_send[5] = (data_type_lsb & 0x00ff0000) >> 16
        bytes_to_send[6] = (data_type_lsb & 0x0000ff00) >> 8
        bytes_to_send[7] = (data_type_lsb & 0x000000ff)
        bytes_to_send[8] = (message.get_target_id() & 0xff000000) >> 24
        bytes_to_send[9] = (message.get_target_id() & 0x00ff0000) >> 16
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

        for x in range(21, self.global_parameter.get_global_datagram_size()):
            bytes_to_send[x] = 0

        return bytes_to_send

    def encode_handshake_commit_message(self, message):
        bytes_to_send = bytearray(self.global_parameter.get_global_datagram_size())

        data_type_msb = message.get_message_id() // (2 ** 32)
        data_type_lsb = message.get_message_id() % (2 ** 32)

        bytes_to_send[0] = (data_type_msb & 0xff000000) >> 24
        bytes_to_send[1] = (data_type_msb & 0x00ff0000) >> 16
        bytes_to_send[2] = (data_type_msb & 0x0000ff00) >> 8
        bytes_to_send[3] = (data_type_msb & 0x000000ff)
        bytes_to_send[4] = (data_type_lsb & 0xff000000) >> 24
        bytes_to_send[5] = (data_type_lsb & 0x00ff0000) >> 16
        bytes_to_send[6] = (data_type_lsb & 0x0000ff00) >> 8
        bytes_to_send[7] = (data_type_lsb & 0x000000ff)
        bytes_to_send[8] = (message.get_target_id() & 0xff000000) >> 24
        bytes_to_send[9] = (message.get_target_id() & 0x00ff0000) >> 16
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

        for x in range(21, self.global_parameter.get_global_datagram_size()):
            bytes_to_send[x] = 0

        return bytes_to_send

    def encode_heartbeat_message(self, message):
        bytes_to_send = bytearray(self.global_parameter.get_global_datagram_size())

        data_type_msb = message.get_message_id() // (2 ** 32)
        data_type_lsb = message.get_message_id() % (2 ** 32)

        bytes_to_send[0] = (data_type_msb & 0xff000000) >> 24
        bytes_to_send[1] = (data_type_msb & 0x00ff0000) >> 16
        bytes_to_send[2] = (data_type_msb & 0x0000ff00) >> 8
        bytes_to_send[3] = (data_type_msb & 0x000000ff)
        bytes_to_send[4] = (data_type_lsb & 0xff000000) >> 24
        bytes_to_send[5] = (data_type_lsb & 0x00ff0000) >> 16
        bytes_to_send[6] = (data_type_lsb & 0x0000ff00) >> 8
        bytes_to_send[7] = (data_type_lsb & 0x000000ff)
        bytes_to_send[8] = (message.get_target_id() & 0xff000000) >> 24
        bytes_to_send[9] = (message.get_target_id() & 0x00ff0000) >> 16
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

        for x in range(21, self.global_parameter.get_global_datagram_size()):
            bytes_to_send[x] = 0

        return bytes_to_send

    def encode_channelopened_message(self, message):
        bytes_to_send = bytearray(self.global_parameter.get_global_datagram_size())

        data_type_msb = message.get_message_id() // (2 ** 32)
        data_type_lsb = message.get_message_id() % (2 ** 32)

        bytes_to_send[0] = (data_type_msb & 0xff000000) >> 24
        bytes_to_send[1] = (data_type_msb & 0x00ff0000) >> 16
        bytes_to_send[2] = (data_type_msb & 0x0000ff00) >> 8
        bytes_to_send[3] = (data_type_msb & 0x000000ff)
        bytes_to_send[4] = (data_type_lsb & 0xff000000) >> 24
        bytes_to_send[5] = (data_type_lsb & 0x00ff0000) >> 16
        bytes_to_send[6] = (data_type_lsb & 0x0000ff00) >> 8
        bytes_to_send[7] = (data_type_lsb & 0x000000ff)
        bytes_to_send[8] = (message.get_target_id() & 0xff000000) >> 24
        bytes_to_send[9] = (message.get_target_id() & 0x00ff0000) >> 16
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

        for x in range(21, self.global_parameter.get_global_datagram_size()):
            bytes_to_send[x] = 0

        return bytes_to_send

    def encode_handshake_message(self, message):
        bytes_to_send = bytearray(self.global_parameter.get_global_datagram_size())

        data_type_msb = message.get_message_id() // (2 ** 32)
        data_type_lsb = message.get_message_id() % (2 ** 32)

        bytes_to_send[0] = (data_type_msb & 0xff000000) >> 24
        bytes_to_send[1] = (data_type_msb & 0x00ff0000) >> 16
        bytes_to_send[2] = (data_type_msb & 0x0000ff00) >> 8
        bytes_to_send[3] = (data_type_msb & 0x000000ff)
        bytes_to_send[4] = (data_type_lsb & 0xff000000) >> 24
        bytes_to_send[5] = (data_type_lsb & 0x00ff0000) >> 16
        bytes_to_send[6] = (data_type_lsb & 0x0000ff00) >> 8
        bytes_to_send[7] = (data_type_lsb & 0x000000ff)
        bytes_to_send[8] = (message.get_target_id() & 0xff000000) >> 24
        bytes_to_send[9] = (message.get_target_id() & 0x00ff0000) >> 16
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

        # body
        ip = message.get_addr()
        port = message.get_port()

        bytes_to_send[21] = ip[0]
        bytes_to_send[22] = ip[1]
        bytes_to_send[23] = ip[2]
        bytes_to_send[24] = ip[3]
        bytes_to_send[25] = port // 256
        bytes_to_send[26] = port % 256

        for x in range(27, self.global_parameter.get_global_datagram_size()):
            bytes_to_send[x] = 0

        return bytes_to_send
