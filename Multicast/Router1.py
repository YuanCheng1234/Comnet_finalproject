

import time
from socket import socket, AF_INET, SOCK_DGRAM
import struct
import select
import random
import asyncore
import threading

import json

def create_dataACK(pketype, SEQ, SRC, DEST):
    '''TYPE = 1B
        SEQ = 1B
        DEST1 = 1B'''
    ACK_packet = struct.pack('BBB', pketype, SEQ, SRC, DEST)
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
        return message.decode('GBK')


if __name__ == '__main__':
    router_receive = socket(AF_INET, SOCK_DGRAM)
    router_receive.bind(('192.168.4.2',1))

    counter = 0
    while counter < 3:
        ACK_packet = receive_router(router_receive)

        send_packet(ACK_packet.encode('GBK'), '192.168.4.3')
        counter += 1















