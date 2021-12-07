class Packet:

    PACKET_TYPE_DICT = {"ACK": 0, "DATA": 1, "EOT": 2}

    def __init__(self, packet_type, seq_num, data):
        self.packet_type = packet_type
        self.seq_num = seq_num
        self.data = data

    def __str__(self):
        return f"Packet Type: {self.packet_type},\n" \
               f"Sequence Number: {self.seq_num},\n" \



class PacketHandler:

    def __init__(self, window_size, payload_data):
        self.window_size = window_size
        self.payload_data = payload_data

    def prepare_packet_list(self):
        packet_list = []
        seq_num_counter = 0
        for data in self.payload_data:
            packet_list.append(Packet(Packet.PACKET_TYPE_DICT["DATA"],
                                      seq_num_counter, data))
            seq_num_counter += 1
        return packet_list

    def __str__(self):
        return f"Window Size: {self.window_size},\n"
