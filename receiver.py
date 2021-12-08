import socket
import time

from packet import PacketType, Packet, encode, decode


class Receiver:
    def __init__(self, sender_ip, sender_port, server_ip, server_port):
        self.sender_ip = sender_ip
        self.sender_port = sender_port
        self.seq_num = 0
        self.sock = None
        self.all_packet = []
        self.fin_recv = False
        self.server_ip = server_ip
        self.server_port = server_port

    def get_sender_ip(self):
        return self.sender_ip

    def set_sock(self, sock):
        self.sock = sock

    def get_sender_port(self):
        return self.sender_port

    def get_seq_num(self):
        return self.seq_num

    def get_sender_asTuple(self):
        return self.sender_ip, self.sender_port

    def increment_seq_num(self):
        self.seq_num += 1

    def send_syn(self):
        syn_packet = encode(Packet(PacketType.SYN, self.seq_num, 0, self.server_ip, self.server_port))
        try:
            self.sock.sendto(syn_packet, self.get_sender_asTuple())
            print("SYN sent")
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
        ack_packet = encode(Packet(PacketType.ACK, self.get_seq_num(), packet.seqNum, self.server_ip, self.server_port))
        self.sock.sendto(ack_packet, self.get_sender_asTuple())
        self.increment_seq_num()
        print(f"ACK sent for packet SEQUENCE NUMBER: {packet.seqNum}")

    def send_eot(self):
        eot_packet = encode(Packet(PacketType.EOT, None, None, self.server_ip, self.server_port))
        self.sock.sendto(eot_packet, self.get_sender_asTuple())
        print(f"EOT sent")

    def wait_for_packets(self):
        packet_recv = []
        while True:
            packet = decode(self.sock.recv(1024))
            while packet.packetType == PacketType.DATA:
                print(f"Received Packet {packet} from {self.get_sender_asTuple()}")
                packet_recv.append(packet)
                packet = decode(self.sock.recv(1024))
            if packet.packetType == PacketType.FIN:
                print("FIN Received")
                self.fin_recv = True
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
        return f"Sender IP and Address {self.get_sender_asTuple()}"


def main():
    NETWORK_PORT = 10000
    NETWORK_IP = "localhost"
    SERVER_PORT = 1
    SERVER_IP = 1
    CLIENT_PORT = 1
    CLIENT_IP = 1

    receiver = Receiver(NETWORK_IP, NETWORK_PORT, SERVER_PORT, SERVER_IP)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((receiver.get_sender_ip(), receiver.get_sender_port()))

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
