
from socket import socket, AF_INET, SOCK_DGRAM

def send_packet(pkt, dst_addr):

    my_socket = socket(AF_INET, SOCK_DGRAM)
    my_socket.sendto(pkt, (dst_addr, 1))
    my_socket.close()
    print("Sent packet to the destination: ", dst_addr)
    return 0


def receive_router(router_receive):

    while True:
        message,addr = router_receive.recvfrom(1024)
        print("Received packet", message, "from source", addr)
        return message.decode('ISO-8859-1')

if __name__ == '__main__':
    router_receive = socket(AF_INET, SOCK_DGRAM)
    router_receive.bind(('192.168.2.3', 1))

    #repeatively forward the ack packet to R1
    data_ACK = receive_router(router_receive)
    send_packet(data_ACK, '192.168.4.2')

