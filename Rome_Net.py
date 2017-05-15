def Rome_Network(wei, xi):

    # this function is used to calculate the maximum loads at each node in the network over the entire duration, the (five)
    # most congested nodes and the edges not utilized 
    
    # all rules for cars leaving and arriving at each node at all times are given in the Project_1.pdf file
    
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
        
        # define the list of number of cars move to the next code at all nodes
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
        # node 13 for the first 180 minutes
        
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
