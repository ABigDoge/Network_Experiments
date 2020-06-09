class Packet: 
    def __init__(self, seqnum, acknum, ack, cwnd):
        self.seqnum = seqnum
        self.acknum = acknum
        self.ack = ack
        self.cwnd = cwnd

def getpkg(seqnum, acknum, ack, cwnd):
    return Packet(seqnum, acknum, ack, cwnd)