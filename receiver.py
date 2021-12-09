import socket
import time

from packet import PacketType, Packet, encode, decode


class Receiver:
    def __init__(self, network_ip, network_port, transmitter_ip, transmitter_port):
        self.network_ip = network_ip
        self.network_port = network_port
        self.seq_num = 0
        self.sock = None
        self.all_packet = []
        self.fin_recv = False
        self.transmitter_ip = transmitter_ip
        self.transmitter_port = transmitter_port

    def get_network_ip(self):
        return self.network_ip

    def set_sock(self, sock):
        self.sock = sock
        self.sock.bind(("localhost", 10000))

    def get_network_port(self):
        return self.network_port

    def get_seq_num(self):
        return self.seq_num

    def get_network_asTuple(self):
        return self.network_ip, self.network_port

    def increment_seq_num(self):
        self.seq_num += 1

    def send_syn(self):
        syn_packet = encode(Packet(PacketType.SYN, self.seq_num, 0, self.transmitter_ip, self.transmitter_port))
        try:
            self.sock.sendto(syn_packet, self.get_network_asTuple())
            print("SYN sent")
            self.increment_seq_num()
            self.send_eot()
        except Exception as e:
            print(e)

    def wait_for_synack(self):
        while True:
            packet = decode(self.sock.recv(1024))
            if packet.packetType == PacketType.SYN_ACK:
                print("SYN/ACK received")
                self.send_ack(packet)  # send ack for the received SYN/ACK
                break
            else:
                time.sleep(5)
                self.send_syn()
        self.send_eot()

    def send_ack(self, packet):
        ack_packet = encode(Packet(PacketType.ACK, self.get_seq_num(), packet.seqNum, self.transmitter_ip, self.transmitter_port))
        self.sock.sendto(ack_packet, self.get_network_asTuple())
        self.increment_seq_num()
        print(f"ACK sent for packet SEQUENCE NUMBER: {packet.seqNum}")

    def send_eot(self):
        eot_packet = encode(Packet(PacketType.EOT, None, None, self.transmitter_ip, self.transmitter_port))
        self.sock.sendto(eot_packet, self.get_network_asTuple())
        print(f"EOT sent")

    def wait_for_packets(self):
        packet_recv = []
        while True:
            packet = decode(self.sock.recv(1024))
            while packet.packetType == PacketType.DATA:
                print(f"Received Packet {packet} from {self.get_network_asTuple()}")
                packet_recv.append(packet)
                packet = decode(self.sock.recv(1024))
            if packet.packetType == PacketType.FIN:
                print("FIN Received")
                self.fin_recv = True
            elif packet.packetType == PacketType.EOT:
                break
        self.duplicate_check(packet_recv)

    def duplicate_check(self, packet_list):
        for i in packet_list:
            self.send_ack(i)
            for j in self.all_packet:
                if i != j:
                    self.all_packet.append(i)
                print(f"Duplicate Detected:\n{j}")
        self.send_eot()

    def __str__(self):
        return f"Sender IP and Address {self.get_network_asTuple()}"


def main():
    NETWORK_PORT = 10004
    NETWORK_IP = "localhost"
    SERVER_PORT = 10005
    SERVER_IP = "localhost"

    receiver = Receiver(NETWORK_IP, NETWORK_PORT, SERVER_IP, SERVER_PORT)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    receiver.set_sock(sock)

    # send syn
    receiver.send_syn()

    # wait for syn/ack
    receiver.wait_for_synack()

    # wait for packets
    while receiver.fin_recv is False:
        receiver.wait_for_packets()


if __name__ == "__main__":
    main()
