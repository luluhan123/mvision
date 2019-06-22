# -*- coding: utf-8 -*-
import threading
import time

from PyQt5.QtCore import QObject, pyqtSignal
from LiENa.LiENaStructure.LiENaDatagram.LienaDecoder import LienaDecoder
from LiENa.LiENaStructure.LiENaMessage.LienaNetworkQualityMessage import LienaNetworkQualityMessage
from LiENa.LiENaStructure.LiENaMessage.LienaChannelReOpenedMessage import LienaChannelReOpenedMessage
from LiENa.LiENaStructure.LiENaMessage.LienaChannelClosedMessage import LienaChannelClosedMessage
from LiENa.LiENaStructure.LiENaMessage.LienaDisengagementMessage import LienaDisengagementMessage
from LiENa.LiENaStructure.LiENaMessage.LienaHandShakeCommitMessage import LienaHandShakeCommitMessage
from LiENa.LiENaStructure.LiENaMessage.LienaHeartbeatMessage import LienaHeartbeatMessage
from LiENa.LiENaStructure.LiENaMessage.LienaHandShakeMessage import LienaHandShakeMessage
from LiENa.LiENaStructure.LiENaMessage.LienaChannelOpenedMessage import LienaChannelOpenedMessage
from LiENa.LiENaStructure.LiENaMessage.LienaReHandshakeCommitMessage import LienaReHandshakeCommitMessage
from LiENa.LiENaStructure.LiENaMessage.lienaReHandshakeMessage import LienaReHandshakeMessage
from LiENa.LiENaStructure.LiENaMessage.LienaDisengagementCommitMessage import LienaDisengagementCommitMessage
from LiENa.LiENaBasic.lienaDefinition import *


class LienaDecodingTask(QObject):

    connectionConfirm = pyqtSignal()
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
    motivateNTPClockSynchronisationMessageArrived = pyqtSignal(LienaNetworkQualityMessage)
    passiveNTPClockSynchronisationMessageArrived = pyqtSignal(LienaNetworkQualityMessage)

    def __init__(self, input_queue, motivate, local_device_id, target_device_id):
        super(LienaDecodingTask, self).__init__()
        self.inputQueue = input_queue
        self.motivate = motivate
        self.localDeviceId = local_device_id
        self.targetDeviceId = target_device_id

        self.decoder = LienaDecoder(motivate, local_device_id, target_device_id)
        self.decoder.channelReOpenedMessageArrived[LienaChannelReOpenedMessage].connect(self.notify_channel_reopened_message_arrived)
        self.decoder.handshakeMessageArrived[LienaHandShakeMessage].connect(self.notify_handshake_message)
        self.decoder.handshakeCommitMessageArrived[LienaHandShakeCommitMessage].connect(self.notify_handshake_commit_message)
        self.decoder.channelOpenedMessageArrived[LienaChannelOpenedMessage].connect(self.notify_channel_opened_message)
        self.decoder.disengagementCommitMessageArrived[LienaDisengagementCommitMessage].connect(self.notify_disengagement_commit_message)
        self.decoder.disengagementMessageArrived[LienaDisengagementMessage].connect(self.notify_disengagement_message)
        self.decoder.channelClosedMessageArrived[LienaChannelClosedMessage].connect(self.notify_channel_closed_message)
        self.decoder.heartBeatMessageArrived[LienaHeartbeatMessage].connect(self.notify_heartbeat_message)
        self.decoder.rehandshakeMessageArrived[LienaReHandshakeMessage].connect(self.notify_rehandshake_message)
        self.decoder.rehandshakeCommitMessageArrived[LienaReHandshakeCommitMessage].connect(self.notify_rehandshake_commit_message)
        self.decoder.passiveNTPClockSynchronisationMessageArrived[LienaNetworkQualityMessage].connect(self.notify_passive_ntp_clock_synchronisation_message)
        self.decoder.motivateNTPClockSynchronisationMessageArrived[LienaNetworkQualityMessage].connect(self.notify_motivate_ntp_clock_synchronisation_message)

        self.rtFlag = True
        self.rtPeriod = 0.05
        self.stand_by = False
        self.receptionTask = threading.Thread(None, self.decode)

    def enable(self):
        self.stand_by = False

    def freeze(self):
        self.stand_by = True

    def notify_channel_reopened_message_arrived(self, msg):
        if DEBUG:
            print("LienaDecodingTask | notifyChannelReOpenedMessageArrived")
        self.channelReOpenedMessageArrived.emit(msg)

    def notify_motivate_ntp_clock_synchronisation_message(self, msg):
        if DEBUG:
            print("LienaDecodingTask | notify_motivate_ntp_clock_synchronisation_message")
        self.motivateNTPClockSynchronisationMessageArrived.emit(msg)

    def notify_passive_ntp_clock_synchronisation_message(self, msg):
        if DEBUG:
            print("LienaDecodingTask | notify_passive_ntp_clock_synchronisation_message")
        self.passiveNTPClockSynchronisationMessageArrived.emit(msg)

    def notify_rehandshake_commit_message(self, msg):
        if DEBUG:
            print("LienaDecodingTask | recovery_down | rehandshakeCommitMessageArrived")
        self.rehandshakeCommitMessageArrived.emit(msg)

    def notify_rehandshake_message(self, msg):
        self.rehandshakeMessageArrived.emit(msg)

    def notify_heartbeat_message(self, msg):
        self.heartBeatMessageArrived.emit(msg)

    def notify_handshake_commit_message(self, msg):
        self.handshakeCommitMessageArrived.emit(msg)

    def notify_channel_closed_message(self, msg):
        self.channelClosedMessageArrived.emit(msg)

    def notify_disengagement_message(self, msg):
        self.disengagementMessageArrived.emit(msg)

    def notify_disengagement_commit_message(self, msg):
        self.disengagementCommitMessageArrived.emit(msg)

    def notify_channel_opened_message(self, msg):
        self.channelOpenedMessageArrived.emit(msg)

    def notify_handshake_message(self, msg):
        if DEBUG:
            print("LienaDecodingTask | notify_handshake_message")

        self.handshakeMessageArrived.emit(msg)

    def launch(self):
        self.receptionTask.start()

    def decode(self):
        while self.rtFlag:

            if self.stand_by:
                time.sleep(1)
                continue

            # send system status to incoming client
            if self.inputQueue.get_length() > 0:
                datagram = self.inputQueue.get_latest_array()
                self.decoder.analyse(datagram)

            time.sleep(self.rtPeriod)

    def set_period(self, rt_period):
        self.rtPeriod = rt_period

    def set_input_cache(self, input_message_cache):
        self.decoder.set_input_cache(input_message_cache)

    def connection_established(self):
        self.connectionConfirm.emit()

    def terminate(self):
        self.rtFlag = False

    def get_handshake_commit_message(self):
        self.decoder.get_handshake_commit_message()
