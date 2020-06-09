import re

info = input("input data to be sent: ")
flag = "7E"
esc = "7D"
print("start flag: {}, data: {}, end flag: {}".format(flag, info, flag))
frame = flag + re.sub(r'({}|{})'.format(flag, esc), r'{}\1'.format(esc), info) + flag
print("frame after byte stuffing: ", frame)
deframe = re.sub(r'{}({}|{})'.format(esc, esc, flag), r'\1', frame[2:-2])
print("frame after deleting bit stuffing: ", deframe)