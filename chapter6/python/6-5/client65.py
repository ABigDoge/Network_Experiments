from socket import *
from tcpPacket import *
import sys
import pickle

ip = sys.argv[1]
host = sys.argv[2]
address = (ip, int(host))
print("target IP: {}, port: {}".format(ip, host))

tcpClientSocket  = socket(AF_INET, SOCK_STREAM)
tcpClientSocket.connect(address)
start = 1

while True:
    if start == 1:
        pkt = getpkg(0, 0, 1, 0)
        print("request for connection: syn({}), ack({})".format(pkt.syn, pkt.ack))
        tcpClientSocket.send(pickle.dumps(pkt))
        start = 0
    data = tcpClientSocket.recv(1024)
    if not data:
        break    
    pkt = pickle.loads(data)
    print("reply for connection: syn({}), ack({})".format(pkt.syn, pkt.ack))
    
tcpClientSocket.close()