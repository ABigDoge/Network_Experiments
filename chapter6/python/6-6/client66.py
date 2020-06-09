from socket import *
from tcpPacket import *
import sys
import pickle
import configparser
import os

ip = '127.0.0.1'
host = 8888
address = (ip, host)

tcpClientSocket  = socket(AF_INET, SOCK_STREAM)
tcpClientSocket.connect(address)

cf = configparser.ConfigParser()
folder = os.path.dirname(os.path.abspath(__file__))
inifile = os.path.join(folder, 'config.ini')
cf.read(inifile)
mss = int(cf.get("congestion", "MSS"))
Threshold = int(cf.get("congestion", "Threshold"))
print("initial MSS: {}, Treshold: {}".format(mss, Threshold))
Threshold = Threshold/mss
TriACKRound = int(cf.get("congestion", "TriACKRound"))
TimeoutRound = int(cf.get("congestion", "TimeoutRound"))
EndRound = int(cf.get("congestion", "EndRound"))

cwndnow = 1
counter = 1

while True:
    if counter == 1:
        newpkt = getpkg(0, 0, 0, cwndnow)
        tcpClientSocket.send(pickle.dumps(newpkt))
    else:
        data = tcpClientSocket.recv(1024) 
        pkt = pickle.loads(data)
        newpkt = getpkg(pkt.acknum, pkt.seqnum+1, 0, cwndnow)
        tcpClientSocket.send(pickle.dumps(newpkt))   
    print("round {}: cwnd size is {} MSS".format(counter, cwndnow))
    
    if counter == EndRound:
        break
    elif counter == TriACKRound:
        print("triple ack!")
        Threshold = int(cwndnow/2)
        cwndnow = Threshold
    elif counter == TimeoutRound:
        print("time out!")
        cwndnow = 1
    elif cwndnow*2 <= Threshold:
        cwndnow = cwndnow*2
    elif cwndnow*2 > Threshold:
        cwndnow  = cwndnow+1

    counter = counter+1
    
tcpClientSocket.close()