import socket, traceback
from UDPtool import *
import crcccitt

host = '127.0.0.1'                             
port = 8888
pktNum = 0

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

while True:
    try:
        pkt,address = receivepkg(s)
        if pkt:
            print("expected packet: ", pktNum)
            print("receive message: ", pkt.mess)
            if crcccitt.calc_crc(pkt.mess) == pkt.crc:
                print("CRC is right")
            else:
                print("CRC is wrong")
            pkt.ip = address[0]
            pkt.port = address[1]
            if pkt.seqnum == pktNum and not pkt.is_corrupt:
                pkt.seqnum = pktNum
                pkt.mess = "ACK " + str(pktNum)
                pkt.crc = crcccitt.calc_crc(pkt.mess)
                pktNum = (pktNum + 1) % 2
            else:
                pkt.mess = "ACK " + str((pktNum + 1) % 2)
                pkt.crc = crcccitt.calc_crc(pkt.mess)
                pkt.seqnum = (pktNum + 1) % 2
                print('corrupt packet: ', pktNum)
            print("next packet to be sent: ", pktNum)
            sendpkg(pkt)
        else:
            print('time is out: ', pktNum)
        
    except (KeyboardInterrupt, SystemExit):
        break
    except:
        traceback.print_exc()
