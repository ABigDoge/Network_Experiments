import traceback
import socket
import random
import time
import pickle

ERRORP = 0.1
LOSTP = 0.1
TIMEOUT = 3
DEBUG = True

class Packet: 
    def __init__(self,mess,seqnum,crc,ip,port):
        self.is_corrupt = False
        self.mess = mess
        self.crc = crc
        self.seqnum = seqnum
        self.ip = ip
        self.port = port

def getpkg(mess,seqnum,crc,ip,port):
    return Packet(mess,seqnum,crc,ip,port)
    
def sendpkg(pkt):

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    time.sleep(random.random())

    if random.random() <= LOSTP:
        if DEBUG:
            print("sending packet is lost: ", pkt.seqnum)
        return s

    if random.random() <= ERRORP:
        if DEBUG:
            print("a corrupt packet is to be sent: ", pkt.seqnum)
        pkt.is_corrupt = True
        pkt.mess = "XXXXX"
        pkt.seqnum = -1
    else:
        if DEBUG:
            print("a normal packet is sent: ", pkt.seqnum)

    s.sendto(pickle.dumps(pkt), (pkt.ip,pkt.port))
    return s

def receivepkg(s):
    s.settimeout(TIMEOUT)
    try:
        data,addr = s.recvfrom(1024)
        pkt = pickle.loads(data)
        return (pkt, addr)

    except socket.timeout:
        print("packet requires to be resent")
    except socket.error:
        traceback.print_exc()

    return (None,None)