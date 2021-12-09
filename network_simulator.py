import random
import socket
import threading

from packet import PacketType, Packet, encode, decode


def dropping_chances(percent):
    rand = random.random() * 100

    if rand < percent:
        return False
    return True


class NetworkSimulator:
    def __init__(self, transmitter_ip, transmitter_port, receiver_ip, receiver_port, loss):
        self.transmitter = (transmitter_ip, transmitter_port)
        self.receiver = (receiver_ip, receiver_port)
        self.receiver_sock = None
        self.transmitter_sock = None
        self.to_be_transmitted = []
        self.packet_loss_percent = loss
        self.fin_recv = False
        self.socket_lock = threading.Lock()

    def get_transmitter(self):
        return self.transmitter

    def get_receiver(self):
        return self.receiver

    def set_socks(self, receiver_sock, transmitter_sock):
        self.receiver_sock = receiver_sock
        self.transmitter_sock = transmitter_sock

    def wait_for_packets(self, sock):
        while True:
            print("Waiting")
            packet, addr = sock.recvfrom(1024)
            packet = decode(packet)
            while True:
                print(f"Received Packet {packet} from {addr}")
                dropped = dropping_chances(self.packet_loss_percent)
                if packet.packetType == PacketType.DATA and dropped is False:
                    self.to_be_transmitted.append(packet)
                if packet.packetType == PacketType.DATA and dropped:
                    packet, addr = sock.recvfrom(1024)
                    packet = decode(packet)
                    print(f"PACKET DROPPED !!")
                if packet.packetType == PacketType.SYN or packet.packetType == PacketType.ACK or packet.packetType == PacketType.SYN_ACK:
                    self.to_be_transmitted.append(packet)
                if packet.packetType == PacketType.FIN or packet.packetType == PacketType.EOT:
                    self.to_be_transmitted.append(packet)
                    if packet.packetType == PacketType.FIN:
                        self.fin_recv = True
                    else:
                        print("EOT received")
                        return False
                packet, addr = sock.recvfrom(1024)
                packet = decode(packet)

    def send_packets(self, sock):
        for i in self.to_be_transmitted:
            sock.sendto(encode(i), (i.endpoint_ip, i.endpoint_port))
            print(f"Sending {i} to {i.endpoint_ip, i.endpoint_port}")
            self.to_be_transmitted.remove(i)


def main():
    NETWORK_PORT = 10002
    NETWORK_IP = "localhost"
    SERVER_PORT = 10003
    SERVER_IP = "localhost"
    CLIENT_PORT = 10004
    CLIENT_IP = "127.0.0.1"
    LOSS = 50

    net_sim = NetworkSimulator(SERVER_IP, SERVER_PORT, CLIENT_IP, CLIENT_PORT, LOSS)

    receive_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    transmit_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    receive_sock.bind((CLIENT_IP, CLIENT_PORT))
    transmit_sock.bind((SERVER_IP, SERVER_PORT))

    while net_sim.fin_recv is False:
        net_sim.wait_for_packets(receive_sock)
        net_sim.send_packets(transmit_sock)
        net_sim.wait_for_packets(receive_sock)
        net_sim.send_packets(transmit_sock)


if __name__ == "__main__":
    main()
