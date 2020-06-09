import numpy as np

maxc = 99
n = 5
disv = [[] for i in range(n)]
nexthop = [[] for i in range(n)]

class Neighbour:
    def __init__(self, num, cost):
        self.num = num
        self.cost = cost

def getdata():
    for i in range(n):
        line = input().split(' ')
        for j in range(len(line)):
            disv[i].append(int(line[j]))
    return

def getnlist():
    nlist = []
    for i in range(n):
        num = []
        cost = []
        for j in range(n):
            nexthop[i].append(-1)
            if disv[i][j]!=maxc and i!=j:
                num.append(j)
                cost.append(disv[i][j])
                nexthop[i][j] = j
        neighb = Neighbour(num, cost)
        nlist.append(neighb)
#    print(nexthop)
    '''
    for i in range(n):
        print(nlist[i].num)
        print(nlist[i].cost)
    '''
        
    return nlist

def printtable(node):
    print("routing table of node {}:".format(node+1))
    for i in range(n):
        nhop = nexthop[node][i]+1
        if i!=node:
            print("forward to node {} to reach {}".format(nhop, i+1))

def learn(node, nb, ct):
    flag = 0
    for i in range(n):
        if disv[node][i] != maxc and ct+disv[node][i] < disv[nb][i]:
            disv[nb][i] = ct + disv[node][i]
            nexthop[nb][i] = node
            flag = 1
    return flag

#node向邻居们发送自己的DV，邻居们进行学习
def sendDV(node):
    updatef = 0
    nbnum = len(nlist[node].num)
    for i in range(nbnum):
        nb = nlist[node].num[i]
        ct = nlist[node].cost[i]
        f = learn(node, nb, ct)
        if f!=0:
            updatef = 1
            print("node {} update distance vector: {}".format(nb+1, disv[nb]))
            printtable(nb)
        #    print("DV after updating: ", disv[nb])
        else:
            print("node {} doesn't make {} to update".format(node+1, nb+1))
    return updatef

getdata()
#print(disv)
nlist = getnlist()
finish = np.zeros(n)
while True:
    print("-----------------------------------------------")
    node = int(input("the node to send DV: "))
    f = sendDV(node-1)
    if f==0:
        finish[node-1] = 1
    #所有都是0，说明没有更新了，收敛了
    if finish.all() == True:
        break;
print("-----------------------------------------------")
print("final distance vector:")
for line in disv:
    print(line)
print("-----------------------------------------------")
print("final routing table:")
for i in range(n):
    printtable(i)