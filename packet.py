import enum
import pickle


class PacketType(enum.Enum):
    SYN = 0
    SYN_ACK = 1
    ACK = 2
    DATA = 3
    FIN = 4
    EOT = 5


class Packet:
    def __init__(self, packet_type, seq_num, ack_num, endpoint_ip, endpoint_port):
        self.packetType = packet_type
        self.ackNum = ack_num
        self.seqNum = seq_num
        if self.packetType == PacketType.SYN:
            self.ackNum = None
            self.seqNum = 0
        self.windowSize = None
        self.data = None
        self.endpoint_ip = endpoint_ip
        self.endpoint_port = endpoint_port

    def set_window_size(self, window_size):
        self.windowSize = window_size

    def set_data(self, data):
        self.data = data

    def __str__(self):
        return f"Type: {self.packetType.name},SeqNum: {self.seqNum},AckNum: {self.ackNum}"


def encode(packet):
    return pickle.dumps(packet)


def decode(packet):
    return pickle.loads(packet)
