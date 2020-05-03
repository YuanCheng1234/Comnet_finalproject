
import time
from socket import socket, AF_INET, SOCK_DGRAM
import struct
import select
import random
import asyncore
import threading
import Queue
import json

def create_dataACK(pketype, SEQ, SRC, DEST):
    '''TYPE = 1B
        SEQ = 1B
        DEST1 = 1B'''
    ACK_packet = struct.pack('BBBB', pketype, SEQ, SRC, DEST)
    return ACK_packet

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
        return message.decode('UTF-8')


if __name__ == '__main__':
    router_receive = socket(AF_INET, SOCK_DGRAM)
    router_receive.bind(('192.168.3.1', 1))
    receive_router(router_receive)
    ACK_packet = create_dataACK(4, 1, 103, 104)

    send_packet(ACK_packet, '192.168.3.2')