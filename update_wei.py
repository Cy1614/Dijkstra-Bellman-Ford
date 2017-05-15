def updateWei(wei,c,xi):

    # this function is for updating the weights of all segments w_{ij} in the network given ta initial weight matrix, an array 
    # of number of cars at all nodes and a parameter xi
    
    # the rule for updating the weight of the path between vertices A and B is given by 
    # wei_new[A,B] = wei_old[A,B] + xi*(c[A]+c[B])/2, where c[A] is the current number of carloads at vertex A, and xi is an
    # given parameter
        
    m, n = np.shape(wei)
    upwei = wei.copy()
    for i in range(m):
        for j in range(n):
            if (upwei[i, j] != 0):
            
                # if currently there is no weight between node i and j, we cannot
                # update the weight w_{ij} since we cannot go straight from i to j
                
                upwei[i, j] = wei[i,j]+xi*(c[i]+c[j])/2
                # update the weights according to the given rule
                
    return upwei
