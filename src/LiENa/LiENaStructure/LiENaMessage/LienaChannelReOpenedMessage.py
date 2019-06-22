from LiENa.LiENaStructure.LiENaMessage.LienaMessage import LienaMessage


class LienaChannelReOpenedMessage(LienaMessage):
    def __init__(self, message_id, target_id, timestamps, dlc):
        LienaMessage.__init__(self, message_id, target_id, timestamps, dlc)
        self.addr = 0
