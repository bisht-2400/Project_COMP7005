import enum


class PacketType(enum.Enum):
    SYN: 0
    SYN_ACK: 1
    ACK: 2
    DATA: 3
    FIN: 4


class Packet:
    def __init__(self, packet_type, seq_num, ack_num, window_size, data):
        self.packetType = packet_type
        self.ackNum = ack_num
        self.seqNum = seq_num
        self.data = data
        self.windowSize = window_size
        if self.packetType == PacketType.SYN:
            self.ackNum = None
            self.seqNum = 0
            self.data = None
