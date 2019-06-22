from LiENa.LiENaStructure.LiENaMessage.LienaMessage import LienaMessage


class LienaHandShakeMessage(LienaMessage):
    def __init__(self, message_id, target_id, timestamps, dlc, _addr, _port):
        LienaMessage.__init__(self, message_id, target_id, timestamps, dlc)

        self.addr = []
        temp = _addr.split(".")
        self.addr.append(int(temp[0]))
        self.addr.append(int(temp[1]))
        self.addr.append(int(temp[2]))
        self.addr.append(int(temp[3]))

        self.port = _port

    def get_addr(self):
        return self.addr

    def get_ip_address(self):
        return str(self.addr[0]) + '.' + str(self.addr[1]) + '.' + str(self.addr[2]) + '.' + str(self.addr[3])

    def set_ip_address(self, address):
        addrs = address.split(".")
        self.addr[0] = int(addrs[0])
        self.addr[1] = int(addrs[1])
        self.addr[2] = int(addrs[2])
        self.addr[3] = int(addrs[3])

    def set_ip_address(self, addr_zero, addr_one, addr_two, addr_three):
        self.addr[0] = addr_zero
        self.addr[1] = addr_one
        self.addr[2] = addr_two
        self.addr[3] = addr_three

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port

    def set_port(self, port_zero, port_one):
        self.port = int(port_zero + port_one)

    def convert_liena_datagram_to_handshake_message(self, datagram):
        if datagram is not None:
            return
        # datagram_body = datagram.get_itc_datagram_body()
        # self.set_ip_address(datagram_body[0], datagram_body[1], datagram_body[2], datagram_body[3])
        # self.set_port(datagram_body[4], datagram_body[5])

        self.message_id = datagram.get_message_id()
        self.target_id = datagram.get_target_id()
        self.timestamps = datagram.get_time_stamps()
        self.dlc = datagram.get_dlc()
