from src.LiENa.LiENaStructure.LiENaMessage.LienaMessage import LienaMessage


class LienaHelloMessage(LienaMessage):
    def __init__(self):
        LienaMessage.__init__(self)
        self.data_type = 0
        self.origine_id = 0
        self.target_id = 0
        self.time_stamps = 0
        self.dlc = 0
        self.body = 1024

    def get_message_id(self):
        return self.data_type

    def set_message_id(self, data_type):
        self.data_type = data_type

    def get_origine_id(self):
        return self.origine_id

    def set_origine_id(self, origine_id):
        self.origine_id = origine_id

    def get_target_id(self):
        return self.target_id

    def set_target_id(self, target_id):
        self.target_id = target_id

    def get_time_stamps(self):
        return self.time_stamps

    def set_time_stamps(self, time_stamps):
        self.time_stamps = time_stamps

    def get_dlc(self):
        return self.dlc

    def set_dlc(self, dlc):
        self.dlc = dlc

    # def get_igt_datagram_body(self):
    #     return self.body
    #
    # def set_igt_datagra_body(self, body):
    #     self.body.replace(0, 4, body)

