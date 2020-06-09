import numpy as np

maxc = 99
n = 5
disv = [[] for i in range(n)]
pathlen = [[] for i in range(n)] 
path = [[] for i in range(n)]
finish = [[] for i in range(n)] 

def getdata():
    for i in range(n):
        line = input().split(' ')
        for j in range(len(line)):
            disv[i].append(int(line[j]))
    return

def getpathlist(path, start, end, pathlist):
    if start == end:
        pathlist.append(start)
    else:
        pathlist.append(end)
        getpathlist(path, start, path[end], pathlist)
    return pathlist

def dijkstra(start, end):
 #   idx = 0
    pathlen.clear()
    path.clear()
    finish.clear()
    for idx in range(n):
        pathlen.append(disv[start][idx])
        finish.append(0)
        path.append(-1)
        if disv[start][idx] < maxc: 
            path[idx] = start
    idx = 1
    finish[start] = 1
    path[start] = 0
    pathlen[start] = 0
    while idx < n:
        minlen = maxc
        for j in range(n):
            if finish[j] == 0 and pathlen[j] < minlen:
                snode = j  
                minlen = pathlen[j]
        finish[snode] = 1
        minlen = maxc 
        for enode in range(n):
            if finish [enode] == 0:
                if disv[snode][enode]<minlen and pathlen[snode]+disv[snode][enode]<pathlen[enode]:
                    pathlen[enode] = pathlen[snode]+disv[snode][enode]
                    path[enode] = snode
        idx += 1
    pathlist = [] 
    pathlist = getpathlist(path, start, end, pathlist)
    return pathlen[end], pathlist

getdata()
rtable = np.zeros((n,n), dtype=np.int)
for i in range(n):
    print('-----------------------------------------------')
    for j in range(n):
        if i != j:
            plen, plist=dijkstra(i,j)
            tmppath = []
            for t in range(len(plist)):
                tmppath.append(plist[len(plist) - 1 - t])
            rtable[i][j] = tmppath[1]
            print("the shortest path from {} to {} is: {}".format(i+1, j+1, tmppath))
            print("the length of the path is: ", plen)
    
print('-----------------------------------------------')
for i in range(n):
    print('routing table of node {}'.format(i+1))
    for j in range(n):
        if i != j:
            print('forward to node {} to reach {}'.format(rtable[i][j]+1, j+1))