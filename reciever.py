from packet import PacketType, Packet


def send_syn():
    syn_packet = Packet(PacketType.SYN, 0, 0, 0, None)
    return syn_packet


def main():
    send_syn()
    #wait for syn/ack
    send_ack()
    #wait for packets
    send_ack()


if __name__ == "__main__":
    main()
