import time
from socket import socket, AF_INET, SOCK_DGRAM
import struct
import select
import random
import asyncore
import threading
import multiprocessing
import json


def create_hello(pkttype, SEQ, SRC):
    '''pkttype = 1B
        scr = 1B
        seq = 1B'''
    Hello_packet = struct.pack('BBB', pkttype, SEQ, SRC)
    return Hello_packet


def read_header(pkt):
    #Change the bytes to account for network encapsulations

    header = pkt[0:3]
    #pktFormat = "BLBBL"
    #pktSize = struct.calcsize(pktFormat)
    pkttype, SEQ, SRC = struct.unpack("BBB", header)
    return  SRC

#def find_shortest_path(Graph, source_num, dest_num):

def create_LSpacket(pketype, SEQ, SRC, LS_data):
    '''pketype = 1B
        seq = 1B
        len = 2B
        src = 1B
        data = 1-1495B = Nodes=ID of all neighbors of SRC and Cost=number of hops to the neighbors'''
    pkelen = len(LS_data)
    LS_header = struct.pack('BBBH', pketype, SEQ, SRC, pkelen)
    LSpacket = LS_header + LS_data.encode('utf-8')
    return LSpacket


def create_datapacket(pketype, SEQ, SRC, NDEST, RDEST, DEST1, DEST2, DEST3, data):
    '''tyep = 1B
        SEQ = 1B
        LEN = 2B
        NDEST=RDEST=DEST1=DEST2=DEST3 = 1B
        DATA = 1-1491B'''
    pkelen = len(data)
    data_packet_header = struct.pack('BBHBBBBBB',pketype, SEQ, pkelen, SRC, NDEST, RDEST, DEST1, DEST2, DEST3)
    return data_packet_header+data


def create_dataACK(pketype, SEQ, SRC, DEST):
    '''TYPE = 1B
        SEQ = 1B
        DEST1 = 1B'''
    ACK_packet = struct.pack('BBB', pketype, SEQ, SRC, DEST)
    return ACK_packet

    #Router receive the data

def send_packet(pkt, dst_addr):

    my_socket = socket(AF_INET, SOCK_DGRAM)
    my_socket.sendto(pkt, (dst_addr, 1))
    my_socket.close()
    print("Sent packet to the destination: ", dst_addr)
    return 0


def receive_router(my_addr, port_num):
    router_receive = socket(AF_INET, SOCK_DGRAM)
    router_receive.bind((my_addr, port_num))
    while True:
        message,addr = router_receive.recvfrom(1024)
        print("Received packet", message, "from source", addr)
        return message.decode('UTF-8')

def get_neighbor(g,start_vertex):
    return g[start_vertex]


if __name__ == '__main__':


    g = {"192.168.4.1": ["192.168.4.2"],
         "192.168.4.2": ["192.168.1.3", "192.168.2.3", "192.168.3.3"],
         "192.168.1.3": ["192.168.1.2", "192.168.4.2"],
         "192.168.1.2": ["192.168.1.1", "192.168.2.2", "192.168.1.3"],
         "192.168.1.1": ["192.168.1.2"],
         "192.168.2.3": ["192.168.2.2"],
         "192.168.2.2": ["192.168.2.1", "192.168.3.2"],
         "192.168.2.1": ["192.168.2.2"],
         "192.168.3.3": ["192.168.3.2"],
         "192.168.3.2": ["192.168.3.1"],
         "192.168.3.1": ["192.168.3.2"]
         }


    # Save the neighbor information in a json file for future use

    #Open the json file
    #f = open("E:\PYTHON\Comnet2_Finalproject\Adjancent.json",)
    #data = json.load(f)
    neighbor_list = get_neighbor(g, '192.168.1.3')


    Hello_packet = create_hello(1, 1, 103)


    print(Hello_packet)

    for node in neighbor_list:

        send_packet(Hello_packet, node)


    counter = 0
    SRC_item = []
    PATHS = []
    COST = []
    while counter < len(neighbor_list):
        Received_packet = receive_router('192.168.1.3', 1)
        # Received_packet = [Received_packet]
        SRC = read_header(Received_packet)

        SRC_item = SRC_item + [SRC]
        counter += 1
    print(SRC_item)


    LS_Packet = create_LSpacket(4, 1, 103, 'DATA')


    for node in neighbor_list:


        send_packet(LS_Packet, node)
