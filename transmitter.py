from packets import Packet
from socket import *


class Transmitter:

    def __init__(self, config_file):
        self.receiver_port = config_file[1]
        self.receiver_address = config_file[2]
        self.transmitter_address = config_file[3]
        self.transmitter_port = config_file[4]
        self.timeout_window = config_file[5]
        self.payload = config_file[6]

    def setup_transmitter(self, sock_obj):
        sock_obj.bind((self.transmitter_address, self.transmitter_port))
        sock_obj.listen(5)

    def send_packet(self, sock_obj, packet):
        try:
            sock_obj.send(packet)
        except error as e:
            print(e)

    def __str__(self):
        return f"Transmitter Port: f{self.transmitter_port},\n" \
               f"Receiver Port: {self.receiver_port},\n" \
               f"Receiver IP Address: {self.receiver_address}\n"





