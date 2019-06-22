import threading


class LienaOutputQueue():
    def __init__(self):
        self.outputQueueLock = threading.Lock()
        self.outputQueue = []

    def append(self, datagram):
        self.outputQueueLock.acquire()
        self.outputQueue.append(datagram)
        self.outputQueueLock.release()

    def get_front_array(self):
        self.outputQueueLock.acquire()
        if len(self.outputQueue) > 0:
            ret = self.outputQueue.pop(0)
        self.outputQueueLock.release()
        return ret

    def get_length(self):
        self.outputQueueLock.acquire()
        length = len(self.outputQueue)
        self.outputQueueLock.release()
        return length

    def clear(self):
        self.outputQueueLock.acquire()
        self.outputQueue = []
        self.outputQueueLock.release()
