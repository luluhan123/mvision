class LienaMessage:
    def __init__(self, message_id, target_id, timestamps, dlc):
        self.message_id = message_id
        self.target_id = target_id
        self.timestamps = timestamps
        self.dlc = dlc

    # def print_self(self):
    #     print(self.message_id, self.target_id, self.timestamps, self.dlc)

    def set_message_id(self, data_type):
        self.message_id = data_type

    def set_target_id(self, target_id):
        self.target_id = target_id

    def set_origin_id(self, origin_id):
        self.origin_id = origin_id

    def set_timestamps(self, timestamps):
        self.timestamps = timestamps

    def set_dlc(self, dlc):
        self.dlc = dlc

    def get_message_id(self):
        return self.message_id

    def get_target_id(self):
        return self.target_id

    def get_origin_id(self):
        return self.origin_id

    def get_timestamps(self):
        return self.timestamps

    def get_dlc(self):
        return self.dlc



