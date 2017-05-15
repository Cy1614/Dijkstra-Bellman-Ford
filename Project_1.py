import sys
import numpy as np
import math as ma
import csv

def Dijkst(ist,isp,wei):
    # Dijkstra algorithm for shortest path in a graph
    #    ist: index of starting node
    #    isp: index of stopping node
    #    wei: weight matrix

    # exception handling (start = stop)
    if (ist == isp):
        shpath = [ist]
        return shpath

    # initialization
    N         =  len(wei)
    Inf       =  sys.maxint
    UnVisited =  np.ones(N,int)
    cost      =  np.ones(N)*1.e6
    par       = -np.ones(N,int)*Inf

    # set the source point and get its (unvisited) neighbors
    jj            = ist
    cost[jj]      = 0
    UnVisited[jj] = 0
    tmp           = UnVisited*wei[jj,:]
    ineigh        = np.array(tmp.nonzero()).flatten()
    L             = np.array(UnVisited.nonzero()).flatten().size

    # start Dijkstra algorithm
    while (L != 0):
        # step 1: update cost of unvisited neighbors,
        #         compare and (maybe) update
        for k in ineigh:
            newcost = cost[jj] + wei[jj,k]
            if ( newcost < cost[k] ):
                cost[k] = newcost
                par[k]  = jj

        # step 2: determine minimum-cost point among UnVisited
        #         vertices and make this point the new point
        icnsdr     = np.array(UnVisited.nonzero()).flatten()
        cmin,icmin = cost[icnsdr].min(0),cost[icnsdr].argmin(0)
        jj         = icnsdr[icmin]

        # step 3: update "visited"-status and determine neighbors of new point
        UnVisited[jj] = 0
        tmp           = UnVisited*wei[jj,:]
        ineigh        = np.array(tmp.nonzero()).flatten()
        L             = np.array(UnVisited.nonzero()).flatten().size

    # determine the shortest path
    shpath = [isp]
    while par[isp] != ist:
        shpath.append(par[isp])
        isp = par[isp]
    shpath.append(ist)

    return shpath[::-1]

def calcWei(RX,RY,RA,RB,RV):
    # calculate the weight matrix between the points

    n    = len(RX)
    wei = np.zeros((n,n),dtype=float)
    m    = len(RA)
    for i in range(m):
        xa = RX[RA[i]-1]
        ya = RY[RA[i]-1]
        xb = RX[RB[i]-1]
        yb = RY[RB[i]-1]
        dd = ma.sqrt((xb-xa)**2 + (yb-ya)**2)
        tt = dd/RV[i]
        wei[RA[i]-1,RB[i]-1] = tt
    return wei
    
def updateWei(wei,c,xi):
    # this function is for updating the weights of all segments w_{ij} in the 
    # network given ta initial weight matrix, an array of number of cars at all
    # 58 nodes and a parameter xi
    m, n = np.shape(wei)
    upwei = wei.copy()
    for i in range(m):
        for j in range(n):
            if (upwei[i, j] != 0):
                # if currently there is no weight between node i and j, we cannot
                # update the weight w_{ij} since we cannot go straight from i 
                # to j
                upwei[i, j] = wei[i,j]+xi*(c[i]+c[j])/2
                # update the weights using the given function upwei[i, j] += ip*(c[i]+c[j])/2
    return upwei
    
def Rome_Network(wei, xi):
    # we are going to use this function to calculate the maximum loads at each
    # node in the network over the 200 iterations, the five most congested nodes
    # and the edges not utilized 
    n = len(wei)
    current_load = np.zeros(n, int)   ####################
    max_load = np.zeros(n, int)       #  initialization  #
    Wei = wei.copy()                  ####################
    U = np.zeros((n, n), int)
    # initialise a zero matrix, which will play a role of an indicator matrix, 
    # i.e, if U[i, j] == 0, it means that there are no cars move from i straight
    # to j over the 200 iterations, and by comparing with the initial weight matrix
    # we can have a list of edges not utilized
    for i in range(1,201):
        move = np.round(current_load*0.7)
        move[51] = np.round(current_load[51]*0.4)
        move = move.astype(int)
        # define the list of number of cars move to the next code of each nodes
        # in the network, special attention paid to the exit node 52 (since only
        # 40% leave at this node), and make the list a list of integers
        arrive = np.zeros(n, int)
        # initialising the number of cars arrive at each of the 58 nodes 
        
        for j in range(n):
            if (current_load[j] != 0):
                path = Dijkst(j, 51, Wei)
                if (len(path) != 1):
                    arrive[path[1]] += move[j]
                    U[j, path[1]] += 1
                else:
                    pass
        # this for loop updates the list "arrive" and the matrix U after using 
        # the Dijkstra's algorithm to compute the optimal path to node 52 from
        # each node of the network except for node 52
        
        current_load += arrive-move # update the car load at each of the nodes
    
        if i <= 180:
            current_load[12] += 20
        else:
            pass
        # this if-statement ensures that 20 cars are injected at the entrance 
        # node 13 for the 180 minutes
        
        for k in range(n):
            if max_load[k] < current_load[k]:
                max_load[k] = current_load[k].copy()
            else:
                pass
        # this for loop updates the maximum number of cars each node loads after
        # each iteration
        
        Wei = updateWei(wei, current_load, xi)
        # use the updateWei function to update the weights of the network after
        # updating the car-load of each nodes in the network

    most_cong = max_load.argsort()[::-1][:5]
    # use argsort() to obtain the indices of the top five nodes based on the 
    # number of cars total loaded by each node
    
    n_utilized = [] # initiasation of a list of edges not utilized during the iterations
    for i in range(n):
        for j in range(n):
            if U[i, j] == 0 and wei[i, j] != 0:
                n_utilized.append([i+1, j+1])
    # the for loop is selecting indices i and j such that no cars move straight 
    # from i to j and there is indeed a path between i and j, then add the path
    # [i, j] to the list "n_utilized"
    
    return max_load, most_cong, n_utilized
    
    

if __name__ == '__main__':
    RomeX = np.empty(0,dtype=float)
    RomeY = np.empty(0,dtype=float)
    with open('RomeVertices','r') as file:
        AAA = csv.reader(file)
        for row in AAA:
            RomeX = np.concatenate((RomeX,[float(row[1])]))
            RomeY = np.concatenate((RomeY,[float(row[2])]))
    file.close()

    RomeA = np.empty(0,dtype=int)
    RomeB = np.empty(0,dtype=int)
    RomeV = np.empty(0,dtype=float)
    with open('RomeEdges','r') as file:
        AAA = csv.reader(file)
        for row in AAA:
            RomeA = np.concatenate((RomeA,[int(row[0])]))
            RomeB = np.concatenate((RomeB,[int(row[1])]))
            RomeV = np.concatenate((RomeV,[float(row[2])]))
    file.close()
    # extract the data from our files and generate RX, RY, RA, RB, RV
    
    wei = calcWei(RomeX,RomeY,RomeA,RomeB,RomeV) # initial weights
    
    max_load_ori, most_cong_ori, n_utilized_ori = Rome_Network(wei, 0.01)
    max_load_new, most_cong_new, n_utilized_new = Rome_Network(wei, 0.)
    # use our function Rome_Network to calculate the maximum load of each node, 
    # most congested nodes and not-utilized edges when xi = 0.01 and xi = 0
    
    block_wei = wei.copy()
    block_wei[29,:] = np.zeros(58)
    block_wei[:,29] = np.zeros(58)
    # update the weight matrix when the accident happens and all routes to or 
    # from node 30 are blocked
    
    max_load_acc,most_cong_acc,_ = Rome_Network(block_wei,0.01)
    max_load_most_cong_acc = max_load_acc[most_cong_acc]
    # compute the maximum load of the most congested nodes
    diff = max_load_acc - max_load_ori 
    # compute the list of changes in the maximum number of cars loaded of each node
    dec_most = diff.argsort()[1]+1
    # compute the list of nodes decrease the most in peak value after the accident, 
    # after intial computation, I found that the first element of this list is 
    # node 30, but we aim to exclude node 30 from the list, hence we take the 
    # first six elements after sorting in descending order then the second element of the
    # list is our target
    inc_most = diff.argsort()[::-1][0]+1
    # compute the node increases the most in peak value after the accident
    
    print 'The maximum load for each node over 200 iterations is: ', max_load_ori
    print 'The five most congested nodes are: ', most_cong_ori+1
    print 'Edges not utilized: ', n_utilized_ori
    
    print 'The maximum load for each node when xi = 0: ', max_load_new
    print 'The five most congested nodes when xi = 0: ', most_cong_new+1
    print 'Edges not utilized when xi = 0: ', n_utilized_new
    
    print 'After accident, the five most congested nodes are: ', most_cong_acc+1
    print 'After accident, the maximum load of the five most congested nodes is: ', max_load_most_cong_acc
    print 'After accident, the nodes decrease the most in peak value are: ', dec_most
    print 'After accident, the nodes increase the most in peak value are: ', inc_most
    # printing our final results
