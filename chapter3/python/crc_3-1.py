import serial
import binascii

def setport(myser):
    print("serial name: ", myser.name)
    myser.baudrate = 9600
    print("serial baudrate: ", myser.baudrate)
    myser.bytesize = 8
    print("serial bytesize: ", myser.bytesize)
    myser.stopbits = 1
    print("serial stopbits: ", myser.stopbits)
    myser.parity = "E"
    print("serial parity: ", myser.parity)
    myser.timeout = 1
    print("serial timeout: ", myser.timeout)
    if myser.isOpen():
        print("open secceed-> ", myser.name)
    else:
        print("open fail-> ", myser.name)

def calc_crc(data):
    crc = 0xFFFF
    for pos in data:
    #    print("pos: ", pos)
        crc ^= pos
        for i in range(8):
            if ((crc & 1) != 0):
                crc >>= 1
                crc ^= 0x8408
            else:
                crc >>= 1
    checksum = ((crc & 0xff) << 8) + (crc >> 8)
#    print("checksum", bin(checksum))
    return checksum

def getcrc(data):
    dd = bytearray.fromhex(data)
#    print("dd: ", dd)
    ddint = int().from_bytes(dd, byteorder='big', signed=True)
    print("data to be sent: {:0>32}".format((bin(ddint)[2:])))
    print("generator: 10001000000100001")
    checksum = calc_crc(dd)
    print("checksum: {:0>16}".format((bin(checksum)[2:])))
    ddint <<= 16
    ret = ddint + checksum
    print("data to be sent with crc code: {:0>48}".format((bin(ret)[2:])))
    return ret

def checkcrc(data):
    checksum = calc_crc(data)
    if checksum == 0:
        print("remainder is zero, CRC right")
        return 1
    else:
        print("remainder is not zero, CRC wrong")
        return 0

'''datasend = "ab"
str_bin = datasend.encode("utf-8")
hexstr = binascii.hexlify(str_bin).decode('utf-8')
print("hex str before CRC: ", hexstr)
crc = hex(getcrc(hexstr))
print("hex str after CRC: ", crc)
#sendd = '0102'
#crc = hex(getcrc(sendd))
rr = crc[2:]
if (len(rr)%2)!=0:
    rr = '0' + rr
print("rr:", rr)
dd = bytearray.fromhex(rr)
print("dd2: ", dd)
lp = checkcrc(dd)'''

ser1 = serial.Serial(port = "COM1")
setport(ser1)
ser2 = serial.Serial(port = "COM2")
setport(ser2)
while True:
    datasend = input("input data to send from COM1: ")
    if datasend == ":quit":
        break
    str_bin = datasend.encode("utf-8")
    hexstr = binascii.hexlify(str_bin).decode('utf-8')
    crc = hex(getcrc(hexstr))
#    print("hex str after CRC: ", crc)
    rr = crc[2:]
    if (len(rr)%2)!=0:
        rr = '0' + rr
    dd = bytearray.fromhex(rr)
#    print("bytes after CRC: ", dd)
    ret = ser1.write(dd)
    datarcv = ser2.readline()
#    print("received data: ", datarcv)
    crcright = checkcrc(datarcv)
    hexrcv = datarcv.hex()
#    print("hex data without crc checksum: ", hexrcv)
    hexb = (hexrcv[:-4]).encode('utf-8')
    revhex = binascii.unhexlify(hexb)
    print("data received: ", revhex)
    print("total bytes: ", ret)
ser1.close()
ser2.close()