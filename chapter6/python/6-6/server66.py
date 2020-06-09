from socket import *
from tcpPacket import *
import sys
import pickle

ip = '127.0.0.1'
host = 8888
address = (ip, host)

tcpServerSocket = socket(AF_INET, SOCK_STREAM)
tcpServerSocket.bind(address)
tcpServerSocket.listen(5)
conn, addr = tcpServerSocket.accept()

while True:
    data = conn.recv(1024)
    if not data:
        break
    pkt = pickle.loads(data)
    newpkt = getpkg(pkt.acknum, pkt.seqnum+1, 1, 0)
    conn.send(pickle.dumps(newpkt))
    
conn.close()
tcpServerSocket.close()