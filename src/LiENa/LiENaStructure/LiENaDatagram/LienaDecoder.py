import time
from PyQt5.QtCore import QObject, pyqtSignal
from LiENa.LiENaStructure.LiENaMessage.LienaChannelClosedMessage import LienaChannelClosedMessage
from LiENa.LiENaStructure.LiENaMessage.LienaDisengagementMessage import LienaDisengagementMessage
from LiENa.LiENaStructure.LiENaMessage.LienaHandShakeCommitMessage import LienaHandShakeCommitMessage
from LiENa.LiENaStructure.LiENaMessage.LienaHeartbeatMessage import LienaHeartbeatMessage
from LiENa.LiENaStructure.LiENaMessage.LienaMotorMsg import LienaMotorMsg
from LiENa.LiENaStructure.LiENaMessage.LienaInjectionMsg import LienaInjectionMsg
from LiENa.LiENaStructure.LiENaMessage.LienaHandShakeMessage import LienaHandShakeMessage
from LiENa.LiENaStructure.LiENaMessage.LienaChannelOpenedMessage import LienaChannelOpenedMessage
from LiENa.LiENaStructure.LiENaMessage.LienaReHandshakeCommitMessage import LienaReHandshakeCommitMessage
from LiENa.LiENaStructure.LiENaMessage.lienaReHandshakeMessage import LienaReHandshakeMessage
from LiENa.LiENaStructure.LiENaMessageStructure.lienaInputMessageCache import LienaInputMessageCache
from LiENa.LiENaStructure.LiENaMessage.LienaDisengagementCommitMessage import LienaDisengagementCommitMessage
from LiENa.LiENaStructure.LiENaMessage.LienaChannelReOpenedMessage import LienaChannelReOpenedMessage
from LiENa.LiENaStructure.LiENaMessage.LienaNetworkQualityMessage import LienaNetworkQualityMessage
from LiENa.LiENaBasic.lienaDefinition import *


class LienaDecoder(QObject):

    handshakeMessageArrived = pyqtSignal(LienaHandShakeMessage)
    rehandshakeMessageArrived = pyqtSignal(LienaReHandshakeMessage)
    rehandshakeCommitMessageArrived = pyqtSignal(LienaReHandshakeCommitMessage)
    channelReOpenedMessageArrived = pyqtSignal(LienaChannelReOpenedMessage)
    heartBeatMessageArrived = pyqtSignal(LienaHeartbeatMessage)
    disengagementMessageArrived = pyqtSignal(LienaDisengagementMessage)
    disengagementCommitMessageArrived = pyqtSignal(LienaDisengagementCommitMessage)
    channelClosedMessageArrived = pyqtSignal(LienaChannelClosedMessage)
    channelOpenedMessageArrived = pyqtSignal(LienaChannelOpenedMessage)
    handshakeCommitMessageArrived = pyqtSignal(LienaHandShakeCommitMessage)
    passiveNTPClockSynchronisationMessageArrived = pyqtSignal(LienaNetworkQualityMessage)
    motivateNTPClockSynchronisationMessageArrived = pyqtSignal(LienaNetworkQualityMessage)

    def __init__(self, motivate, local_device_id, target_device_id):
        super(LienaDecoder, self).__init__()

        self.motivate = motivate
        self.localDeviceId = local_device_id
        self.targetDeviceID = target_device_id
        self.inputMessageCache = LienaInputMessageCache()

        self.port = None
        self.addr = None

    def analyse(self, datagram):
        customized_message_id = datagram.get_customized_message_id()
        # target_id = datagram.get_target_id()

        if DEBUG:
            print("analyse | customized message id", customized_message_id)

        if customized_message_id == LIENA_SESSION_MANAGEMENT_HANDSHAKE_MESSAGE:
            self.convert_lienadatagram_to_handshake_message(datagram)

        elif customized_message_id == LIENA_SESSION_MANAGEMENT_HANDSHAKE_COMMIT_MESSAGE:
            self.convert_lienadatagram_to_handshakecommitmessage(datagram)

        elif customized_message_id == LIENA_SESSION_MANAGEMENT_DISENGAGEMENT_MESSAGE:
            self.convert_lienadatagram_to_disengagementmessage(datagram)

        elif customized_message_id == LIENA_SESSION_MANAGEMENT_CHANNEL_OPENED_MESSAGE:
            self.convert_lienadatagram_to_channel_opened_message(datagram)

        elif customized_message_id == LIENA_SESSION_MANAGEMENT_CHANNEL_CLOSED_MESSAGE:
            self.convert_lienadatagram_to_channel_closed_message(datagram)

        elif customized_message_id == LIENA_SESSION_MANAGEMENT_DISENGAGEMENTCOMMIT_MESSAGE:
            self.convert_lienadatagram_to_disengagement_commit_message(datagram)

        elif customized_message_id == LIENA_SESSION_MANAGEMENT_HEARTBEAT_MESSAGE:
            self.convert_lienadatagram_to_heartbeat_message(datagram)

        elif customized_message_id == LIENA_SESSION_MANAGEMENT_REHANDSHAKE_MESSAGE:
            self.convert_lienadatagram_to_rehandshake_message(datagram)

        elif customized_message_id == LIENA_SESSION_MANAGEMENT_REHANDSHAKECOMMIT_MESSAGE:
            self.convert_lienadatagram_to_rehandshake_commit_message(datagram)

        elif customized_message_id == LIENA_SESSION_MANAGEMENT_CHANNEL_REOPENED_MESSAGE:
            self.convert_lienadatagram_to_channel_reopened_message(datagram)

        elif customized_message_id == LIENA_SESSION_MANAGEMENT_NTP_CLOCK_SYNCHRONIZATION_MESSAGE:
            self.convert_lienadatagram_to_network_quality_message(datagram)

    def convert_lienadatagram_to_network_quality_message(self, datagram):
        message_id = datagram.get_message_id()
        target_id = datagram.get_target_id()
        time_stamps = datagram.get_time_stamps()
        dlc = datagram.get_dlc()
        body = datagram.get_body()

        if DEBUG:
            print("LienaDecoder | convert_lienadatagram_to_network_quality_message |", message_id)

        if datagram.get_customized_message_id() == LIENA_SESSION_MANAGEMENT_NTP_CLOCK_SYNCHRONIZATION_MESSAGE:
            if datagram.get_origin_id() == self.localDeviceId:

                index = int(body[0])
                t1 = int(body[1]) * (256 ** 4) + int(body[2]) * (256 ** 3) + int(body[3]) * (256 ** 2) + int(body[4]) * (256 ** 1) + int(body[5]) * (256 ** 0)
                t2 = int(body[6]) * (256 ** 4) + int(body[7]) * (256 ** 3) + int(body[8]) * (256 ** 2) + int(body[9]) * (256 ** 1) + int(body[10]) * (256 ** 0)
                t3 = int(body[11]) * (256 ** 4) + int(body[12]) * (256 ** 3) + int(body[13]) * (256 ** 2) + int(body[14]) * (256 ** 1) + int(body[15]) * (256 ** 0)
                t4 = int(body[16]) * (256 ** 4) + int(body[17]) * (256 ** 3) + int(body[18]) * (256 ** 2) + int(body[19]) * (256 ** 1) + int(body[20]) * (256 ** 0)
                print(index, "message back", t1, t2, t3, t4)
                network_quality_message = LienaNetworkQualityMessage(message_id, target_id, time_stamps, dlc)
                network_quality_message.set_index(index)
                network_quality_message.set_t1(t1)
                network_quality_message.set_t2(t2)
                network_quality_message.set_t3(t3)
                network_quality_message.set_t4(t4)
                self.motivateNTPClockSynchronisationMessageArrived.emit(network_quality_message)
            else:
                index = int(body[0])
                t1 = int(body[1]) * (256 ** 4) + int(body[2]) * (256 ** 3) + int(body[3]) * (256 ** 2) + int(body[4]) * (256 ** 1) + int(body[5]) * (256 ** 0)
                t2 = int(body[6]) * (256 ** 4) + int(body[7]) * (256 ** 3) + int(body[8]) * (256 ** 2) + int(body[9]) * (256 ** 1) + int(body[10]) * (256 ** 0)
                network_quality_message = LienaNetworkQualityMessage(message_id, target_id, time_stamps, dlc)
                network_quality_message.set_index(index)
                network_quality_message.set_t1(t1)
                network_quality_message.set_t2(t2)
                self.passiveNTPClockSynchronisationMessageArrived.emit(network_quality_message)

    def convert_lienadatagram_to_channel_reopened_message(self, datagram):
        message_id = datagram.get_message_id()
        target_id = datagram.get_target_id()
        time_stamps = datagram.get_time_stamps()
        dlc = datagram.get_dlc()

        if DEBUG:
            print("LienaDecoder | convert_lienadatagram_to_channel_reopened_message |", message_id)

        channel_reopened_message = LienaChannelReOpenedMessage(message_id, target_id, time_stamps, dlc)
        self.channelReOpenedMessageArrived.emit(channel_reopened_message)

    def convert_lienadatagram_to_rehandshake_commit_message(self, datagram):
        message_id = datagram.get_message_id()
        target_id = datagram.get_target_id()
        time_stamps = datagram.get_time_stamps()
        dlc = datagram.get_dlc()

        if DEBUG:
            print("LienaDecoder | convert_lienadatagram_to_rehandshake_message |", message_id)

        rehandshake_commit_message = LienaReHandshakeCommitMessage(message_id, target_id, time_stamps, dlc)
        self.rehandshakeCommitMessageArrived.emit(rehandshake_commit_message)

    def convert_lienadatagram_to_rehandshake_message(self, datagram):
        message_id = datagram.get_message_id()
        target_id = datagram.get_target_id()
        time_stamps = datagram.get_time_stamps()
        dlc = datagram.get_dlc()

        if DEBUG:
            print("LienaDecoder | convert_lienadatagram_to_rehandshake_message |", message_id)

        rehandshake_message = LienaReHandshakeMessage(message_id, target_id, time_stamps, dlc)
        self.rehandshakeMessageArrived.emit(rehandshake_message)

    def convert_lienadatagram_to_heartbeat_message(self, datagram):
        message_id = datagram.get_message_id()
        target_id = datagram.get_target_id()
        time_stamps = datagram.get_time_stamps()
        dlc = datagram.get_dlc()

        if DEBUG:
            print("LienaDecoder | convert_lienadatagram_to_heartbeat_message |", message_id)
            print("heartbeat message latency: ", round((time.time() % 86400) * 1000000) - time_stamps)

        heart_beat_message = LienaHeartbeatMessage(message_id, target_id, time_stamps, dlc)
        self.heartBeatMessageArrived.emit(heart_beat_message)

    def convert_lienadatagram_to_disengagementmessage(self, datagram):
        message_id = datagram.get_message_id()
        target_id = datagram.get_target_id()
        time_stamps = datagram.get_time_stamps()
        dlc = datagram.get_dlc()

        if DEBUG:
            print("LienaDecoder | convert_lienadatagram_to_disengagement_message |", message_id)

        disengagement_message = LienaDisengagementMessage(message_id, target_id, time_stamps, dlc)
        self.disengagementMessageArrived.emit(disengagement_message)

    def convert_lienadatagram_to_disengagement_commit_message(self, datagram):
        message_id = datagram.get_message_id()
        target_id = datagram.get_target_id()
        time_stamps = datagram.get_time_stamps()
        dlc = datagram.get_dlc()

        if DEBUG:
            print("LienaDecoder | convert_lienadatagram_to_disengagement_commit_message |", message_id)

        message = LienaDisengagementCommitMessage(message_id, target_id, time_stamps, dlc)
        self.disengagementCommitMessageArrived.emit(message)

    def convert_lienadatagram_to_channel_closed_message(self, datagram):
        message_id = datagram.get_message_id()
        target_id = datagram.get_target_id()
        time_stamps = datagram.get_time_stamps()
        dlc = datagram.get_dlc()

        if DEBUG:
            print("LienaDecoder | convert_lienadatagram_to_channel_closed_message |", message_id)

        message = LienaChannelClosedMessage(message_id, target_id, time_stamps, dlc)
        self.channelClosedMessageArrived.emit(message)

    def convert_lienadatagram_to_channel_opened_message(self, datagram):
        if DEBUG:
            print("LienaDecoder | convert_lienadatagram_to_channelOpenedMessage |")

        message_id = datagram.get_message_id()
        target_id = datagram.get_target_id()
        time_stamps = datagram.get_time_stamps()
        dlc = datagram.get_dlc()

        channel_opened_message = LienaChannelOpenedMessage(message_id, target_id, time_stamps, dlc)
        self.channelOpenedMessageArrived.emit(channel_opened_message)

    def convert_lienadatagram_to_handshake_message(self, datagram):
        message_id = datagram.get_message_id()
        target_id = datagram.get_target_id()
        time_stamps = datagram.get_time_stamps()
        dlc = datagram.get_dlc()
        body = datagram.get_body()

        addr = str(int(body[0])) + '.' + str(int(body[1])) + '.' + str(int(body[2])) + '.' + str(int(body[3]))
        port = body[4]*256 + body[5]

        if True:
            print("convert_lienadatagram_to_handshake_message", addr, port)

        handshake_message = LienaHandShakeMessage(message_id, target_id, time_stamps, dlc, addr, port)
        self.handshakeMessageArrived.emit(handshake_message)

    def convert_lienadatagram_to_handshakecommitmessage(self, datagram):
        if DEBUG:
            print("convert_lienadatagram_to_handshakecommitmessage")
        message_id = datagram.get_message_id()
        target_id = datagram.get_target_id()
        time_stamps = datagram.get_time_stamps()
        dlc = datagram.get_dlc()

        body = datagram.get_body()

        handshake_commit_msg = LienaHandShakeCommitMessage(message_id, target_id, time_stamps, dlc)
        # handshake_commit_msg.transform_datagram_to_handshake_commit_message(datagram)
        self.handshakeCommitMessageArrived.emit(handshake_commit_msg)

    def set_handshake_message(self, handshake_message):
        self.handshake_messgae = handshake_message

    def get_handshake_message(self):
        return self.handshake_message

    def set_handshake_commit_message(self,handshake_commit_msg):
        self.handshake_messgae = handshake_commit_msg

    def get_handshake_commit_message(self):
        return self.handshake_commit_msg

    def get_handshake_commit_addr(self):
        return self.addr

    def get_handshake_commit_port(self):
        return self.port

    def decode_injection_message(self, datagram):
        datagram_body = datagram.get_itc_datagram_body()
        injection_msg = LienaInjectionMsg(datagram)
        self.context.append_new_injection_msg(injection_msg)

    def decode_close_session_message(self, datagram):
        datagram_body = datagram.get_itc_datagram_body()
        if DEBUG:
            print("close session message ...")
        self.parent.close_session()

    def decode_hello_message(self, datagram):
        x = 1

    def decode_motor_message(self, datagram):

        motor_msg = LienaMotorMsg(datagram)

        if self.switcher_instruction[motor_msg.motor_type] == "catheterMoveInstruction":
            self.context.append_new_catheter_move_message(motor_msg)
        elif self.switcher_instruction[motor_msg.motor_type] == "guidewireProgressInstruction":
            self.context.append_new_guidewire_progress_move_message(motor_msg)
        elif self.switcher_instruction[motor_msg.motor_type] == "guidewireRotateInstruction":
            self.context.append_new_guidewire_rotate_move_message(motor_msg)
        elif self.switcher_instruction[motor_msg.motor_type] == "contrastMediaPushInstruction":
            self.context.append_new_contrast_media_push_move_message(motor_msg)
        elif self.switcher_instruction[motor_msg.motor_type] == "retractInstruction":
            self.context.append_latest_retract_message(motor_msg)

    def set_input_cache(self, inputMessageCache):
        self.inputMessageCache = inputMessageCache
