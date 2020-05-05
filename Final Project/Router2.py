
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
        return message.decode('GBK')

if __name__ == '__main__':
    #forward data packet to dest 1
    router_receive = socket(AF_INET, SOCK_DGRAM)
    router_receive.bind(('192.168.1.4', 1))
    #receive forward packet
    data_packet = receive_router(router_receive)
    send_packet(data_packet.encode('GBK'), '192.168.1.3')


    #repeatively forward the ack packet to R2
    data_ACK = receive_router(router_receive)
    send_packet(data_ACK.encode('GBK'), '192.168.4.2')