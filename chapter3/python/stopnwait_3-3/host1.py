import socket
import traceback
from UDPtool import *
import crcccitt

global pktNum 
pktNum = 0

def sendrun(someMsg):
    host = '127.0.0.1'                          
    port = 8888
    sendf = True 
    global pktNum 
    while sendf:
        try:
            crc = crcccitt.calc_crc(someMsg)
            pkt = getpkg(someMsg,pktNum,crc,host,port)
            sock = sendpkg(pkt) 
            pkt,addr = receivepkg(sock)
            if pkt:
                print("expected ACK packet: ", pktNum)
                if not pkt.is_corrupt or pkt.seqnum != pktNum:
                    if "ACK" in pkt.mess and str(pktNum) in pkt.mess:
                        pktNum = (pktNum + 1) % 2
                        print("receive ACK:", pkt.mess)
                        sendf = False
                    else:
                        print("not ACK: ", pktNum)
                else:
                    print('corrupt packet: ', pktNum)
                if crcccitt.calc_crc(pkt.mess) == pkt.crc:
                    print("CRC is right")
                else:
                    print("CRC is wrong")
                print("next packet to be sent: ", pktNum)
            else:
                print('time is out: ', pktNum)
        except (KeyboardInterrupt, SystemExit):
            break
        except:
            traceback.print_exc()

def main():
    message = "This is a test string message for computer network assignment"    
    for word in message.split(sep=" "):
        sendrun(word)
    
    
if __name__ == '__main__':
    main()