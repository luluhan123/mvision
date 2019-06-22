from src.LiENa.LiENaStructure.LiENaMessage.LienaMessage import LienaMessage


class LienaOmegaPositionMessage(LienaMessage):
    def __init__(self):
        LienaMessage.__init__(self)
        self.px = 0
        self.py = 0
        self.pz = 0

    def set_position_x(self, px):
        self.px = px

    def get_position_x(self):
        return self.px

    def set_position_y(self, py):
        self.py = py

    def get_position_y(self):
        return self.py

    def set_position_z(self, pz):
        self.pz = pz

    def get_position_z(self):
        return self.pz
