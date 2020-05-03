
from socket import socket, AF_INET, SOCK_DGRAM
import codecs

def send_packet(pkt, dst_addr):

    my_socket = socket(AF_INET, SOCK_DGRAM)
    my_socket.sendto(pkt, (dst_addr, 1))
    my_socket.close()
    print("Sent packet to the destination: ", dst_addr)
    return 0


def receive_router(my_addre, port):
    router_receive = socket(AF_INET, SOCK_DGRAM)
    router_receive.bind((my_addre, port))
    while True:
        message,addr = router_receive.recvfrom(1024)
        print("Received packet", message, "from source", addr)

        return codecs.decode(message, 'GBK')

if __name__ == '__main__':


    #repeatively forward the ack packet to R1
    data_ACK = receive_router('192.168.2.3',1)
    send_packet(data_ACK.encode('GBK'), '192.168.4.2')

