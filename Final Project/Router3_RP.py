import time
from socket import socket, AF_INET, SOCK_DGRAM
import struct
import select
import random
import asyncore
import threading

import json

#-*- coding : utf-8-*-
# coding:unicode_escape

def create_packet(pkttype, SEQ, SRC):
    """Create a new packet based on given id"""
    # Type(1),  LEN(4), SRCID(1),  DSTID(1), SEQ(4), DATA(1000)

    header = struct.pack('BBB', pkttype, SEQ, SRC)
    return header



#def find_shortest_path(Graph, source_num, dest_num):

def create_LSpacket(pketype, SEQ, SRC, LS_data):
    '''pketype = 1B
        seq = 1B
        len = 2B
        src = 1B
        data = 1-1495B = Nodes=ID of all neighbors of SRC and Cost=number of hops to the neighbors'''
    pkelen = len(LS_data)
    LS_header = struct.pack('BBBH', pketype, SEQ, SRC, pkelen)
    LSpacket = LS_header + LS_data
    return LSpacket


def create_datapacket(pketype, SEQ, SRC, NDEST, RDEST, DEST1, DEST2, DEST3, data):
    '''tyep = 1B
        SEQ = 1B
        LEN = 2B
        NDEST=RDEST=DEST1=DEST2=DEST3 = 1B
        DATA = 1-1491B'''
    pkelen = len(data)
    data_packet_header = struct.pack("BBHBBBBBB",pketype, SEQ, pkelen, SRC, NDEST, RDEST, DEST1, DEST2, DEST3)
    return data_packet_header+data


def create_dataACK(pketype, SEQ, SRC, DEST):
    '''TYPE = 1B
        SEQ = 1B
        DEST1 = 1B'''
    ACK_packet = struct.pack('BBBB', pketype, SEQ, SRC, DEST)
    return ACK_packet

def read_header(pkt):
    #Change the bytes to account for network encapsulations
    header = pkt[0:10]
    #pktFormat = "BLBBL"
    #pktSize = struct.calcsize(pktFormat)
    pketype, SEQ, pkelen, SRC, NDEST, RDEST, DEST1, DEST2, DEST3 = struct.unpack("BBHBBBBBB", header)
    return NDEST


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

def get_neighbor(g,start_vertex):
    return g[start_vertex]


if __name__ == '__main__':
    #send data packet to dest2
    router_receive = socket(AF_INET, SOCK_DGRAM)
    router_receive.bind(('192.168.4.1', 1))

    data_packet = receive_router(router_receive)

    #send ack back to R3
    data_ACK = create_dataACK (4, 1, 206, 104)
    send_packet(data_ACK,'192.168.4.2')

    NDEST = read_header(data_packet)
    #from RP, send packet to R5, R7, D2
    Host = ['192.168.2.2','192.168.1.4','192.168.3.2']
    if NDEST == 2:
        selected_host = random.sample(Host, 2)

        for dest in selected_host:
            send_packet(data_packet, dest)

    elif NDEST == 3:
        for dest in Host:
            send_packet(data_packet, dest)

    #start receiving and sending the ack packet
    while True:
        ACK_packet = receive_router(router_receive)
        send_packet(ACK_packet.encode('GBK'), '192.168.4.2')






