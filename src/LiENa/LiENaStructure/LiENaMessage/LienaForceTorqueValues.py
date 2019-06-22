from src.LiENa.LiENaStructure.LiENaMessage.LienaMessage import LienaMessage


class LienaForceTorqueValues(LienaMessage):
    def __init__(self):
        LienaMessage.__init__(self)
        self.fx = 0.0
        self.fy = 0.0
        self.fz = 0.0
        self.tx = 0.0
        self.ty = 0.0
        self.tz = 0.0

    def set_force_back_x(self,fx):
        self.fx = fx

    def set_force_back_y(self, fy):
        self.fy = fy

    def set_force_back_z(self, fz):
        self.fz = fz

    def set_torque_feedback_x(self, tx):
        self.tx = tx

    def set_torque_feedback_y(self, ty):
        self.ty = ty

    def set_torque_feedback_z(self, tz):
        self.tz = tz

    def get_force_back_x(self):
        return self.fx

    def get_force_back_y(self):
        return self.fy

    def get_force_back_z(self):
        return self.fz

    def get_torque_feedback_x(self):
        return self.tx

    def get_torque_feedback_y(self):
        return self.ty

    def get_torque_feedback_z(self):
        return self.tz