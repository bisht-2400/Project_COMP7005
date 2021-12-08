import socket
from random import randrange

from packet import PacketType, Packet, encode, decode


def dropping_chances(percent):
    value = 0
    value *= 100
    if value < percent:
        return True
    return False


class NetworkSimulator:
    def __init__(self, server_ip, server_port, client_ip, client_port, loss):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_ip = client_ip
        self.client_port = client_port
        self.to_be_transmitted = []
        self.packet_loss_percent = loss
        self.fin_recv = False

    def get_server_ip(self):
        return self.server_ip

    def get_server_port(self):
        return self.server_port

    def get_client_ip(self):
        return self.client_ip

    def get_client_port(self):
        return self.client_port

    def get_packets(self, sock):
        while True:
            print("Waiting")
            packet = sock.recv(1024)
            packet = decode(packet)
            print("Done waiting", packet)
            while True:
                print(f"Received Packet {packet} from {packet.endpoint_ip, packet.endpoint_port}")
                if packet.packetType == PacketType.DATA and dropping_chances(self.packet_loss_percent):
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
            sock.sendto(i, (i.endpoint_ip, i.endpoint_port))
            print(f"Sending {i} to {i.endpoint_ip, i.endpoint_port}")


def main():
    NETWORK_PORT = 10000
    NETWORK_IP = "localhost"
    SERVER_PORT = 10000
    SERVER_IP = "localhost"
    CLIENT_PORT = 10001
    CLIENT_IP = "127.0.0.1"
    LOSS = 50

    net_sim = NetworkSimulator(SERVER_IP, SERVER_PORT, CLIENT_IP, CLIENT_PORT, LOSS)

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_sock.bind((net_sim.get_server_ip(), net_sim.get_server_port()))
    client_sock.bind((CLIENT_IP, CLIENT_PORT))

    while net_sim.fin_recv is False:
        net_sim.get_packets(client_sock)
        net_sim.send_packets(server_sock)
        net_sim.get_packets(server_sock)
        net_sim.send_packets(client_sock)


if __name__ == "__main__":
    main()
