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
