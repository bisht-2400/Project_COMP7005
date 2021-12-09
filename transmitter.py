from packets import Packet
import socket


from packet import PacketType, Packet, encode, decode
import configuration


class Transmitter:

    def __init__(self, receiver_port, receiver_address, network_address, network_port,
                 timeout_window):
        self.receiver_port = receiver_port
        self.receiver_address = receiver_address
        self.network_address = network_address
        self.network_port = network_port
        self.timeout_window = timeout_window
        self.payload = None
        self.sock_obj = None

    def get_network_details(self):
        return self.network_address, self.network_port

    def send_syn_ack(self):
        syn_ack_packet = encode(Packet(PacketType.SYN_ACK, 1, 0,
                                       self.receiver_address, self.receiver_port))
        try:
            self.sock_obj.sendto(syn_ack_packet, self.get_network_details())
            print("SYN-ACK sent")
        except Exception as e:
            print(e)

    def send_ack(self, packet):
        ack_packet = encode(Packet(PacketType.ACK, 1, packet.seqNum,
                                   self.receiver_address, self.receiver_port))
        self.sock_obj.sendto(ack_packet, self.get_network_details())
        print(f"ACK sent for packet SEQUENCE NUMBER: {packet.seqNum}")

    def wait_for_syn(self):
        syn_received = False
        print("Waiting for syn...")
        while not syn_received:
            packet = self.sock_obj.recv(1024)
            current_packet = decode(packet)
            if current_packet.packetType == PacketType.SYN:
                self.send_syn_ack()
            syn_received = True

    def set_sock_obj(self, sock_obj):
        self.sock_obj = sock_obj
        self.sock_obj.bind(("localhost", 10005))

    def send_packet(self, sock_obj, packet):
        try:
            sock_obj.send(packet)
        except Exception as e:
            print(e)

    def __str__(self):
        return f"Transmitter Port: f{self.network_port},\n" \
               f"Receiver Port: {self.receiver_port},\n" \
               f"Receiver IP Address: {self.receiver_address}\n"


def main():
    config = configuration.Configuration()
    transmitter = Transmitter(config.receiver_port, config.receiver_ip,
                              config.network_ip, config.network_port,
                              5)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    transmitter.set_sock_obj(sock)
    transmitter.wait_for_syn()


if __name__ == '__main__':
    main()
