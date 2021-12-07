import socket

from packet import PacketType, Packet, encode


def send_syn():
    syn_packet = Packet(PacketType.SYN, 0, 0, 0, None)
    return encode(syn_packet)


def main():
    NETWORK_PORT = 4440
    NETWORK_IP = "localhost"
    SERVER_PORT = 1
    SERVER_IP = 1
    CLIENT_PORT = 1
    CLIENT_IP = 1

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.sendto(send_syn(), (NETWORK_IP, NETWORK_PORT))

    # wait for syn/ack
    wait_for_synack()

    # send_ack()
    # wait for packets
    # send_ack()


if __name__ == "__main__":
    main()
