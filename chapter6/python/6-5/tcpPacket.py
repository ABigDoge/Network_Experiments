class Packet: 
    def __init__(self, seqnum, acknum, syn, ack):
        self.seqnum = seqnum
        self.acknum = acknum
        self.syn = syn
        self.ack = ack

def getpkg(seqnum, acknum, syn, ack):
    return Packet(seqnum, acknum, syn, ack)