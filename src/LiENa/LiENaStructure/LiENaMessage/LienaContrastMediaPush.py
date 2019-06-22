from src.LiENa.LiENaStructure.LiENaMessage.LienaMessage import LienaMessage


class LienaContrastMediaPush(LienaMessage):
    def __init__(self):
        LienaMessage.__init__(self)

        self.speed = 0.0
        self.volume = 0.0

    def set_speed(self,speed):
        self.speed = speed

    def get_speed(self):
        return self.speed

    def set_volume(self,volume):
        self.volume = volume

    def get_volume(self):
        return self.volume