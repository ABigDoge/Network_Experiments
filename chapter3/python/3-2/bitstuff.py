info = input("input data to be sent: ")
flag = "01111110"
print("start flag: {}, data: {}, end flag: {}".format(flag, info, flag))
frame = flag + info.replace('11111', '111110') + flag
print("frame after bit stuffing: ", frame)
deframe = frame[8:-8].replace('111110','11111')
print("frame after deleting bit stuffing: ", deframe)