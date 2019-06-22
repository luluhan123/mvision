from src.LiENa.LiENaStructure.LiENaMessage.LienaMessage import LienaMessage


class LienaFastenContrastMediaPush(LienaMessage):
    def __init__(self):
        LienaMessage.__init__(self)

        self.control_flag = 0

    def set_control_flag(self,control_flag):
        self.control_flag = control_flag

    def get_control_flag(self):
        return self.control_flag