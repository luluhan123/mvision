from LiENa.LiENaStructure.LiENaMessage.LienaMessage import LienaMessage


class LienaReHandshakeCommitMessage(LienaMessage):
    def __init__(self, message_id, target_id, timestamps, dlc):
        LienaMessage.__init__(self, message_id, target_id, timestamps, dlc)
        self.count = 0
