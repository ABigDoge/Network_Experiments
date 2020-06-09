import serial

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

ser1 = serial.Serial(port = "COM1")
setport(ser1)
ser2 = serial.Serial(port = "COM2")
setport(ser2)
while True:
    datasend = input("input data to send from COM1: ")
    if datasend == ":quit":
        break
    ret = ser1.write(datasend.encode('utf-8'))
    datarcv = ser2.readline()
    print("received data: ", datarcv.decode('utf-8'))
    print("total bytes: ", ret)
ser1.close()
ser2.close()