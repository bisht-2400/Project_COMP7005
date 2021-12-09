import socket
import threading
from random import randrange

from packet import PacketType, Packet, encode, decode


def dropping_chances(percent):
    value = 0
    value *= 100
    if value < percent:
        return True
    return False


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
            packet = sock.recv(1024)
            packet = decode(packet)
            print("Done waiting", packet)
            while True:
                print(f"Received Packet {packet} from {packet.endpoint_ip, packet.endpoint_port}")
                if packet.packetType == PacketType.DATA and dropping_chances(self.packet_loss_percent):
                    self.to_be_transmitted.append(packet)
                self.to_be_transmitted.append(packet)
                packet = decode(sock.recv(1024))
                if packet.packetType == PacketType.FIN or packet.packetType == PacketType.EOT:
                    if packet.packetType == PacketType.FIN:
                        self.fin_recv = True
                    self.to_be_transmitted.append(packet)
                    print("EOT received", self.to_be_transmitted)
                    return False

    def send_packets(self, sock):
        for i in self.to_be_transmitted:
            sock.sendto(encode(i), (i.endpoint_ip, i.endpoint_port))
            print(f"Sending {i} to {i.endpoint_ip, i.endpoint_port}")


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
