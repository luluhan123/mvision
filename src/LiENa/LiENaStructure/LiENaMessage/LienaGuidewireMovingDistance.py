from src.LiENa.LiENaStructure.LiENaMessage.LienaMessage import LienaMessage


class LienaGuidewireMovingDistance(LienaMessage):
    def __init__(self):
        LienaMessage.__init__(self)
        self.value =0
        self.unit = 0
        self.speed =0

    def set_speed(self,speed):
        self.speed = speed

    def get_speed(self):
        return self.speed

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def set_unit(self, unit):
        self.unit = unit

    def get_unit(self):
        return self.unit

    def transform_igt_datagram_to_distance(self,datagram):
        datagram_body = datagram.get_itc_datagram_body()
        self.set_value(datagram_body[0])