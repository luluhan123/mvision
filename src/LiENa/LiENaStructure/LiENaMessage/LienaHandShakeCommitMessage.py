from LiENa.LiENaStructure.LiENaMessage.LienaMessage import LienaMessage
from LiENa.LiENaStructure.LiENaDatagram import LienaDatagram


class LienaHandShakeCommitMessage(LienaMessage):
    def __init__(self, message_id, target_id, timestamps, dlc):
        LienaMessage.__init__(self, message_id, target_id, timestamps, dlc)
        self.addr = 0
