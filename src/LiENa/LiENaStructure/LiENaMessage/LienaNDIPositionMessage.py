from src.LiENa.LiENaStructure.LiENaMessage.LienaMessage import LienaMessage


class LienaNDIPositionMessage(LienaMessage):
    def __init__(self):
        LienaMessage.__init__(self)
        self.position_x = 0
        self.position_y = 0
        self.position_z = 0

        self.times_stamps = 0.0

    def set_position_x(self, position_x):
        self.position_x = position_x

    def get_position_x(self):
        return self.position_x

    def set_position_y(self, position_y):
        self.position_y = position_y

    def get_position_y(self):
        return self.position_y

    def set_position_z(self, position_z):
        self.position_z = position_z

    def get_position_z(self):
        return self.position_z

    def set_times_stamps(self, times_stamps):
        self.times_stamps = times_stamps

    def get_times_stamps(self):
        return self.times_stamps