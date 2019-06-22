import time


class LienaGlobal:
    def __init__(self):
        self.global_datagram_size = 1024
        self.global_port = 10704
        self.global_clock_offset = 0
        self.localDeviceId = 0

    def set_local_device_id(self, local_device_id):
        self.localDeviceId = local_device_id

    def set_global_datagram_size(self, global_datagram_size):
        self.global_datagram_size = global_datagram_size

    def set_global_port(self, global_port):
        self.global_port = global_port

    def get_local_device_id(self):
        return self.localDeviceId

    def get_global_datagram_size(self):
        return self.global_datagram_size

    def get_global_port(self):
        return self.global_port

    def get_current_time_in_microsecond(self):
        return round((time.time() % 86400) * 1000000) - self.global_clock_offset
