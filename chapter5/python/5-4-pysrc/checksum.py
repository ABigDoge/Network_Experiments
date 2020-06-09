import configparser
import os
import struct
import socket

def getcs(header):
    cs = []
    for i in range(0, 40, 4):
        cs.append(int(header[i:i+4], 16))
    cs = sum([i for i in cs]) - cs[5]
    if cs > 0xffff:
        cs = int(hex(cs)[2], 16) + int(hex(cs)[3:], 16)
    return cs ^ 0xffff
    
def printinfo():
    cf = configparser.ConfigParser()
    folder = os.path.dirname(os.path.abspath(__file__))
    inifile = os.path.join(folder, 'config.ini')
    cf.read(inifile)
    header = cf.get("checksum", "IPHeader")
    print("IP header: {}".format(header))
    print("Version: {}".format(int(header[0:1], 16)))
    print("Header Length: {}".format(int(header[1:2],16)))
    print("Type of Service: {}".format(int(header[2:4],16)))
    print("Total Length: {}".format(int(header[4:8],16)))
    print("Identifier: {}".format(int(header[8:12],16)))
    print("Flags: {}".format(int(header[12:13],16)))
    print("Fragmented Offset: {}".format(int(header[13:16],16)))
    print("Time to Live: {}".format(int(header[16:18],16)))
    print("Protocal: {}".format(int(header[18:20],16)))
    print("Header Checksum: {}".format(int(header[20:24],16)))
    print("Source IP: {}".format(socket.inet_ntoa(struct.pack("!I", int(header[24:32], 16)))))
    print("Destination IP: {}".format(socket.inet_ntoa(struct.pack("!I", int(header[32:40], 16)))))
    print("---------calculate checksum----------")
    print(hex(getcs(header)))

printinfo()