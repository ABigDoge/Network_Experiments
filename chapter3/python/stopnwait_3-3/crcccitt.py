import binascii

def calc_crc(data):
    str_bin = data.encode("utf-8")
    hexstr = binascii.hexlify(str_bin).decode('utf-8')
    dd = bytearray.fromhex(hexstr)
    crc = 0xFFFF
    for pos in dd:
    #    print("pos: ", pos)
        crc ^= pos
        for i in range(8):
            if ((crc & 1) != 0):
                crc >>= 1
                crc ^= 0x8408
            else:
                crc >>= 1
    checksum = ((crc & 0xff) << 8) + (crc >> 8)
    crcstr = bin(checksum)[2:]
    return crcstr