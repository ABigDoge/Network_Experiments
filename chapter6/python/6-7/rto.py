import configparser
import os

def getconfig():
    cf = configparser.ConfigParser()
    folder = os.path.dirname(os.path.abspath(__file__))
    inifile = os.path.join(folder, 'config.ini')
    cf.read(inifile)
    alpha = float(cf.get("rto", "Alpha"))
    beita = float(cf.get("rto", "Beita"))
    rttlist = cf.get("rto", "RTT")
    rtt = rttlist.split(',')
    rtt = [ float(i) for i in rtt ]
    return alpha, beita, rtt

def cal():
    alpha, beita, rtt = getconfig()
    eRTT = rtt[0]
    devRTT = rtt[0]/2
    rto = eRTT + 4*devRTT
    rttnum = len(rtt)
    print("initial:\nsRTT: {:.2f}, eRTT: {:.2f}, RTO: {:.2f}".format(rtt[0],eRTT,rto))
    for i in range(1, rttnum):
        eRTT = (1-alpha)*eRTT + alpha*rtt[i]
        devRTT = (1-beita)*devRTT + beita*abs(rtt[i]-eRTT)
        rto = eRTT + 4*devRTT
        print("round {}:\nsRTT: {:.2f}, eRTT: {:.2f}, RTO: {:.2f}".format(i,rtt[i],eRTT,rto))

cal()