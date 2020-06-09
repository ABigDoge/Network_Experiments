import configparser
import os
import math

def printinfo(tlen, iden, df, mf, offset):
    print("Total length of the packet: {}".format(tlen))
    print("Identification: {}".format(iden))
    print("flags: DF({}) MF({})".format(df, mf))
    print("offset: {}".format(offset))

def fragment():
    cf = configparser.ConfigParser()
    folder = os.path.dirname(os.path.abspath(__file__))
    inifile = os.path.join(folder, 'config.ini')
    cf.read(inifile)
#    print(cf.sections())   
    BigIPTotalLen = int(cf.get("fragment", "BigIPTotalLen"))
    Iden = int(cf.get("fragment", "ID"))
    MTU = int(cf.get("fragment", "MTU"))
    print("original big packet:")
    printinfo(BigIPTotalLen, Iden, 0, 0, 0)
    print("MTU: {}".format(MTU))

    print("--------after fragmentation--------")
    fragnum = math.ceil((BigIPTotalLen-20)/(MTU-20))
    print("FragNum: {}".format(fragnum))
    for i in range(fragnum):
        print("small packet {}:".format(i+1))
        if i < fragnum-1:
            slen = MTU
            mf = 1
        else:
            slen = (fragnum-1)*20 + BigIPTotalLen - MTU*(fragnum-1)
            mf = 0
        offset = int(i*(MTU-20)/8)
        printinfo(slen, Iden, 0, mf, offset)
    
def reassembly():
    cf = configparser.ConfigParser()
    folder = os.path.dirname(os.path.abspath(__file__))
    inifile = os.path.join(folder, 'config.ini')
    cf.read(inifile)
    fragnum = int(cf.get("reassembly", "FragNum"))
    totallen = cf.get("reassembly", "TotalLen")
    slen = totallen.split(',')
    slen = [ int(i) for i in slen ]
    fragid = cf.get("reassembly", "ID")
    idlist = fragid.split(',')
    fragmf = cf.get("reassembly", "FragMF")
    mf = fragmf.split(',')
    FragOffset = cf.get("reassembly", "FragOffset")
    offset = FragOffset.split(',')

    biglen = 0
    for i in range(fragnum):
        print("small packet {}:".format(i+1))
        printinfo(slen[i], idlist[i], 0, mf[i], offset[i])
        biglen += slen[i]
    biglen -= (fragnum-1)*20

    print("-------after reassembly-------")
    printinfo(biglen, idlist[0], 0, 0, 0)

fragment()
print()
reassembly()