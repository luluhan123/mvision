from LiENa.LiENaStructure.LiENaMessage.LienaMessage import LienaMessage


class LienaNetworkQualityMessage(LienaMessage):
    def __init__(self, message_id, target_id, timestamps, dlc):
        LienaMessage.__init__(self, message_id, target_id, timestamps, dlc)
        self.index = 0
        self.t1 = 0
        self.t2 = 0
        self.t3 = 0
        self.t4 = 0

    def get_index(self):
        return self.index

    def set_index(self, index):
        self.index = index

    def set_t1(self, t1):
        self.t1 = t1

    def set_t2(self, t2):
        self.t2 = t2

    def set_t3(self, t3):
        self.t3 = t3

    def set_t4(self, t4):
        self.t4 = t4

    def get_t1(self):
        return self.t1

    def get_t2(self):
        return self.t2

    def get_t3(self):
        return self.t3

    def get_t4(self):
        return self.t4
