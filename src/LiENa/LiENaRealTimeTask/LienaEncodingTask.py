# -*- coding: utf-8 -*-
import threading
import time
from LiENa.LiENaBasic.lienaDefinition import *
from LiENa.LiENaStructure.LiENaDatagram.LienaEncoder import LienaEncoder
from LiENa.LiENaStructure.LiENaMessage.LienaHandShakeMessage import LienaHandShakeMessage
from LiENa.LiENaStructure.LiENaMessage.LienaChannelOpenedMessage import LienaChannelOpenedMessage
from LiENa.LiENaStructure.LiENaMessage.LienaHandShakeCommitMessage import LienaHandShakeCommitMessage
from LiENa.LiENaStructure.LiENaMessage.LienaDisengagementCommitMessage import LienaDisengagementCommitMessage
from LiENa.LiENaStructure.LiENaMessage.LienaDisengagementMessage import LienaDisengagementMessage
from LiENa.LiENaStructure.LiENaMessage.LienaChannelClosedMessage import LienaChannelClosedMessage
from LiENa.LiENaStructure.LiENaMessage.LienaReHandshakeCommitMessage import LienaReHandshakeCommitMessage
from LiENa.LiENaStructure.LiENaMessage.LienaChannelReOpenedMessage import LienaChannelReOpenedMessage
from LiENa.LiENaStructure.LiENaMessage.lienaReHandshakeMessage import LienaReHandshakeMessage


class LienaEncodingTask:
    def __init__(self, output_queue, global_parameter, motivate, target_device_id):
        self.output_queue = output_queue
        self.global_parameter = global_parameter
        self.motivate = motivate
        self.targetDeviceId = target_device_id
        self.encoder = LienaEncoder(self.global_parameter)

        self.stand_by = False

        self.outputMessageCache = None
        self.rtPeriod = 0.05

        self.flag = True
        self.encodingThread = threading.Thread(None, self.encode)

    def enable(self):
        self.stand_by = False

    def freeze(self):
        self.stand_by = True

    def send_channel_opened_message(self):
        if DEBUG:
            print("LienaEncodingTask | send_channel_opened_message")

        message_id = self.global_parameter.get_local_device_id() * (2 ** 32) + LIENA_SESSION_MANAGEMENT_CHANNEL_OPENED_MESSAGE
        target_device_id = self.targetDeviceId
        timestamps = round((time.time() % 86400) * 1000000)

        channel_opened_message = LienaChannelOpenedMessage(message_id, target_device_id, timestamps, 6)
        datagram = self.encoder.encode(channel_opened_message)
        self.output_queue.append(datagram)

    def send_disengagement_message(self):
        if DEBUG:
            print("LienaEncodingTask | send_disengagement_message")

        message_id = self.global_parameter.get_local_device_id() * (2 ** 32) + LIENA_SESSION_MANAGEMENT_DISENGAGEMENT_MESSAGE
        target_device_id = self.targetDeviceId
        timestamps = round((time.time() % 86400) * 1000000)
        disengagement_message = LienaDisengagementMessage(message_id, target_device_id, timestamps, 6)
        
        datagram = self.encoder.encode(disengagement_message)
        self.output_queue.append(datagram)

    def send_channel_repaired_message(self):
        if DEBUG:
            print("LienaEncodingTask | send_channel_repaired_message")

        message_id = self.global_parameter.get_local_device_id() * (2 ** 32) + LIENA_SESSION_MANAGEMENT_CHANNEL_REOPENED_MESSAGE
        target_device_id = self.targetDeviceId
        timestamps = round((time.time() % 86400) * 1000000)
        disengagement_message = LienaChannelReOpenedMessage(message_id, target_device_id, timestamps, 6)

        datagram = self.encoder.encode(disengagement_message)
        self.output_queue.append(datagram)

    def send_rehandshake_commit_message(self):
        if DEBUG:
            print("LienaEncodingTask | send_rehandshake_commit_message")

        message_id = self.global_parameter.get_local_device_id() * (2 ** 32) + LIENA_SESSION_MANAGEMENT_REHANDSHAKECOMMIT_MESSAGE
        target_device_id = self.targetDeviceId
        timestamps = round((time.time() % 86400) * 1000000)
        message = LienaReHandshakeCommitMessage(message_id, target_device_id, timestamps, 6)

        datagram = self.encoder.encode(message)
        self.output_queue.append(datagram)

    def send_disengagement_commit_message(self):
        if DEBUG:
            print("LienaEncodingTask | send_disengagement_commit_message")

        message_id = self.global_parameter.get_local_device_id() * (2 ** 32) + LIENA_SESSION_MANAGEMENT_DISENGAGEMENTCOMMIT_MESSAGE
        target_device_id = self.targetDeviceId
        timestamps = round((time.time() % 86400) * 1000000)
        message = LienaDisengagementCommitMessage(message_id, target_device_id, timestamps, 6)

        datagram = self.encoder.encode(message)
        self.output_queue.append(datagram)

    def send_back_network_quality_message(self, msg):
        datagram = self.encoder.encode(msg)
        self.output_queue.append(datagram)

    def send_rehandshake_message(self):
        if DEBUG:
            print("LienaEncodingTask | send_rehandshake_message")

        message_id = self.global_parameter.get_local_device_id() * (2 ** 32) + LIENA_SESSION_MANAGEMENT_REHANDSHAKE_MESSAGE
        target_device_id = self.targetDeviceId
        timestamps = round((time.time() % 86400) * 1000000)
        message = LienaReHandshakeMessage(message_id, target_device_id, timestamps, 6)

        datagram = self.encoder.encode(message)
        self.output_queue.append(datagram)

    def send_channel_closed_message(self):
        if DEBUG:
            print("LienaEncodingTask | send_channel_closed_message")

        message_id = self.global_parameter.get_local_device_id() * (2 ** 32) + LIENA_SESSION_MANAGEMENT_CHANNEL_CLOSED_MESSAGE
        target_device_id = self.targetDeviceId
        timestamps = round((time.time() % 86400) * 1000000)
        channel_closed_message = LienaChannelClosedMessage(message_id, target_device_id, timestamps, 6)

        datagram = self.encoder.encode(channel_closed_message)
        self.output_queue.append(datagram)

    def send_handshake_commit_message(self):
        if DEBUG:
            print("LienaEncodingTask | send_handshake_commit_message")
        message_id = self.global_parameter.get_local_device_id() * (2 ** 32) + LIENA_SESSION_MANAGEMENT_HANDSHAKE_COMMIT_MESSAGE
        target_device_id = self.targetDeviceId
        timestamps = round((time.time() % 86400) * 1000000)
        handshake_commit_message = LienaHandShakeCommitMessage(message_id, target_device_id, timestamps, 6)

        datagram = self.encoder.encode(handshake_commit_message)
        self.output_queue.append(datagram)

    def send_handshake_message(self, addr):
        if DEBUG:
            print("LienaEncodingTask | new_send_handshake_message")

        message_id = self.global_parameter.get_local_device_id()*(2**32) + LIENA_SESSION_MANAGEMENT_HANDSHAKE_MESSAGE
        target_device_id = self.targetDeviceId
        timestamps = round((time.time() % 86400) * 1000000)
        handshake_message = LienaHandShakeMessage(message_id, target_device_id, timestamps, 6, addr, 10704)

        datagram = self.encoder.encode(handshake_message)
        self.output_queue.append(datagram)

    def launch(self):
        self.encodingThread.start()

    def set_output_cache(self, output_message_cache):
        self.outputMessageCache = output_message_cache

    def terminate(self):
        self.flag = False

    def encode(self):
        while self.flag:

            if self.stand_by:
                time.sleep(1)
                continue

            # send system status to incoming client
            # if self.output_queue.get_length() > 0:
            #     for cpt in range(0, self.output_queue.get_length()):
            #         print "decoding.."
            #         # if self.outputMessageCache.get_latest_guidewire_moving_distance_sequence_length() > 0:
            #         #     msg = self.outputMessageCache.fetch_latest_guidewire_moving_distance_msg()
            #         #     self.output_queue_manager.add_datagram_by_id(cpt, msg)

            time.sleep(self.rtPeriod)
