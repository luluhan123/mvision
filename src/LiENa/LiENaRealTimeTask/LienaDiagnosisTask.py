import threading
import time
from PyQt5.QtCore import QObject, pyqtSignal
from LiENa.LiENaBasic.lienaDefinition import *


class LienaDiagnosisTask(QObject):

    lostConnexion = pyqtSignal()

    def __init__(self):
        super(LienaDiagnosisTask, self).__init__()
        self.heartBeatMessageListLock = threading.Lock()
        self.heartBeatMessageList = []
        self.flag = False
        self.heartBeatMessageArrived = False

        self.connection_failed = False

        self.period = 2
        self.connexionStatus = 1
        self.heartBeatMessageCount = 0

    def heartbeat_message_arrived(self):
        return self.heartBeatMessageArrived

    def set_period(self, period):
        self.period = period

    def terminate(self):
        self.flag = False

    def launch(self):
        self.flag = True
        self.heartBeatMessageList = []
        self.connexionStatus = 1
        task = threading.Thread(None, self.diagnosis)
        task.start()

    def get_sequence_length(self):
        self.heartBeatMessageListLock.acquire()
        ret = len(self.heartBeatMessageList)
        self.heartBeatMessageListLock.release()
        return ret

    def get_latest_message(self):
        ret = None
        self.heartBeatMessageListLock.acquire()
        ret = self.heartBeatMessageList.pop(0)
        self.heartBeatMessageListLock.release()
        return ret

    def append(self, msg):
        self.heartBeatMessageCount += 1
        self.heartBeatMessageListLock.acquire()
        self.heartBeatMessageList.append(msg)
        self.heartBeatMessageListLock.release()

        if self.heartBeatMessageCount == 1:
            if DEBUG:
                print("diagnosis task launched")
            self.launch()

    def connection_failed_recovery(self):
        self.connection_failed = False

    def diagnosis(self):
        while self.flag:

            if self.connection_failed:
                print("LienaDiagnosisTask | wait for network failure handling ")
                time.sleep(1)
                continue

            if self.get_sequence_length() > 0:
                self.connexionStatus = 1
                msg = self.get_latest_message()
            elif self.get_sequence_length() == 0:
                self.connexionStatus *= 2
                if self.connexionStatus > 8:
                    self.lostConnexion.emit()
                    self.connexionStatus = 1
                    self.connection_failed = True

            time.sleep(self.period)
