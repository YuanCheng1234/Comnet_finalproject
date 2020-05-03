import time
from socket import socket, AF_INET, SOCK_DGRAM
import struct
import select
import random
import asyncore
import threading
import Queue
import json
my_queue = Queue.Queue()

def storeInQueue(f):
  def wrapper(*args):
    my_queue.put(f(*args))
  return wrapper


def create_packet(pkttype, SEQ, SRC):
    """Create a new packet based on given id"""
    # Type(1),  LEN(4), SRCID(1),  DSTID(1), SEQ(4), DATA(1000)

    header = struct.pack('BBB', pkttype, SEQ, SRC)
    return header



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
    LSpacket = LS_header + LS_data
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

    router_receive = socket(AF_INET, SOCK_DGRAM)
    router_receive.bind(('192.168.4.3', 1))
    k_val = input('Please input the number of k: ')
    host = ['192.168.1.1','192.168.2.1','192.168.3.1']
    Data_packet = create_datapacket(3, 1, 104, k_val, 1, 101, 102, 103, 'DATA')

    if k_val == 1:
        #unicast to one dest
        dest = random.sample(host, 1)
        send_packet(Data_packet, dest)
    elif k_val == 2:
        #send to RP
        send_packet(Data_packet, '192.168.2.2')

    elif k_val == 3:
        #send to RP
        send_packet(Data_packet, '192.168.2.2')


    #start receiving ack packets
    while True:
        receive_router(router_receive)






