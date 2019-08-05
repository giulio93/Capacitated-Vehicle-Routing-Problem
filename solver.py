import numpy as np
from cvrpGraph import cvrpGraph
import operator
from route import Route
import parser as par
import math


def printResult(folderSol,folderRes):

    #path='./mysol_DJ_kRand'
    path = folderRes
    mysol = par.readInstanceList(path)
    #path2='./cvrp-sol'
    path2 = folderSol
    cvrp_sol = par.readInstanceList(path2)
    for sol in mysol:
        with open(path+'/'+sol, "r+") as f:
            for line in f:
                keywords = line
                if(keywords.split(':')[0].strip()=="Routing Total Cost"):
                    stimated = float(keywords.split(':')[1].strip())
                    for optimal in cvrp_sol:
                        with open(path2+'/'+optimal, "r") as c:
                            if(sol.split('.')[0] == "Sol_"+optimal.split('.')[0]):
                                for linec in c:
                                    keys = linec                                   
                                    if(len(keys.split()) > 0 and keys.split()[0].strip()=="Cost"):
                                        actual = float(keys.split()[1].strip())
                                        error = (stimated - actual)/actual
                                        print("Error of solution in "+sol + ": "+ str(float(error)))
                                        f.write("Error of solution in "+sol + ": "+ str(float(error)))

def ClarkeWright(graph):
    print("Clarke & Wright have been evoked!")

    dimension = graph.getDimension()
    demand = graph.getDemand()
    depot = graph.getDepot()

    savings = []
    for i in range(1,dimension):
        for j in range(1,dimension):
            if i!=j:
                save = graph.getValue(i,0) + graph.getValue(0,j) - graph.getValue(i,j)
                savings.append((float(save), i, j))

    savings.sort(key=lambda x: x[0], reverse=True)

    routes = []
    for x in range(1, dimension):
        appoRoute =  Route(graph.getCapacity()) 
        appoRoute.addCustomer(x,demand[x],False)
        routes.append(appoRoute)

    for save in savings:
        i = save[1]
        j = save[2]
        customerI = -1
        customerJ = -1
        routeA = -1
        routeB = -1

        # no routes have been created yet
        if len(routes) == 0:
            firstRoute =  Route(graph.getCapacity())
            firstRoute.addCustomer(i,demand[i],True)
            firstRoute.addCustomer(j,demand[j],False)
            routes.append(firstRoute)
        else:
            #check if customer i and j have been already served
            for route in routes:
                if(-2< customerI < 0):
                    customerI = route.checkCustomer(i)
                    routeA = route
                if(-2< customerJ < 0):
                    customerJ = route.checkCustomer(j)
                    routeB = route
                #check if i and j have been served by a single route
                  
            # case: i and j have not been served yet
            if(-2 < customerI < 0  and -2 < customerJ < 0):
                newRoute =  Route(graph.getCapacity())
                control1 =  newRoute.addCustomer(i,demand[i],False)
                control2 =  newRoute.addCustomer(j,demand[j],False)
                # No constraint violated on the route
                if(control1 != -1 and control2 != -1):
                    routes.append(newRoute)
            #customer i is served but j not.
            if (customerI >= 0 and customerJ == -1):
                if(customerI == 0):
                    route.addCustomer(j,demand[j],True)
                else:
                    route.addCustomer(j,demand[j],False)
            #customer j is served but i not.
            if (customerI == -1 and customerJ >= 0):
                if(customerJ == 0):
                  route.addCustomer(i,demand[i],True)
                else:
                  route.addCustomer(i,demand[i],False)

            # both i and j have been served already, but from different routes, MERGE them
            if (customerI >= 0 and customerJ >= 0 and routeA != -1 and routeB!= -1) :
                if (routes.index(routeA) != routes.index(routeB)):
                    # Does routeA and routeB merge's overload final route
                    if(routeA.getPayload() + routeB.getPayload() <= graph.getCapacity()):
                        #The edge that connect routeA to routeB resides in their heads
                        if(customerI == 0 and customerJ == 0):                     
                            for customer in routeA.getCustomers():
                                routeB.addCustomer(customer,demand[customer],True)
                            routes.remove(routeA)
                        
                        #The edge that connect routeA to routeB resides in head of routeA and tail of routeB
                        if(customerI == 0 and customerJ > 0):                     
                            for customer in routeA.getCustomers():
                                routeB.addCustomer(customer,demand[customer],False)
                            routes.remove(routeA)
       
                        #The edge that connect routeA to routeB resides in head of routeB and tail of routeA
                        if(customerI > 0 and customerJ == 0):                     
                            for customer in routeB.getCustomers():
                                routeA.addCustomer(customer,demand[customer],False)
                            routes.remove(routeB)

                        #The edge that connect routeA to routeB resides in their tails
                        if(customerI > 0 and customerJ > 0):                     
                            for customer in reversed(routeB.getCustomers()):
                                routeA.addCustomer(customer,demand[customer],False)
                            routes.remove(routeB)

            print("Savings number :" + str(savings.index(save)))    
            #savings.remove(save) 
    
    #If a node is has not been served yet, let's add a route just for it
    for node in range(1,graph.getDimension() -1):
        checked = False
        for r in routes:
            if node in r.getCustomers():
                checked = True
        if (checked == False):
            adhocRoute =  Route(graph.getCapacity())
            control1 =  adhocRoute.addCustomer(node,demand[node],False)
            routes.append(adhocRoute)



   
    #Finile routing adding connection to the Depot, print Route path and cost in a file
    routeCost = 0  
    routedNodesControl = 1
    f= open("mysol/Sol_"+graph.getFileName()+".txt","w+")
    f.write(str(graph.name)+"\n")
    f.write(str(graph.dimension)+"\n")
    
    for fianlRoute in routes:
        fianlRoute.addCustomer(0,0,True)
        fianlRoute.addCustomer(0,0,False)        
        appo = fianlRoute.printRoute(routes.index(fianlRoute))
        f.write(appo+"\n")
        for i in range(len(fianlRoute.getCustomers())-1):
            routedNodesControl = routedNodesControl +1
            routeCost += graph.getValue(fianlRoute.getCustomers()[i], fianlRoute.getCustomers()[i+1])
        routedNodesControl = routedNodesControl -1 

          
    f.write("Total Routed Nodes "+ str(routedNodesControl)+"\n")
    f.write("Routing Total Cost: "+ str(routeCost)+"\n")


def FisherJaikumar_Kselector(graph,n_vehicles):

    dimension = graph.getDimension()
    capacity = graph.getCapacity()
    demand = graph.getDemand()
    depot = graph.getDepot()
    maxCoverDistance = graph.getArgMaxDistance()
    seeds = []
    treshold = capacity/2
    depotDistance = []
    scaledown = 2
    for c in range(dimension):
        depotDistance.append(graph.getValue(0,c))

    scannerRadius = depotDistance.copy()
    appo =  depotDistance.copy()

    #select K seeds
    while len(seeds) < n_vehicles  or np.max(scannerRadius)==0:
        candidates = []
        if( sum(demand) != dimension-1):
            for i in range(dimension):
                if (demand[i] > capacity/scaledown):
                    candidates.append(i)
        else:
            candidates = np.arange(dimension)

        for c in sorted(candidates):           
            if(depotDistance[c] >= np.max(scannerRadius)):
                if len(seeds) == 0:
                    seeds.append(c)
                    scannerRadius[c] = 0
                    #depotDistance[c] = 0
                    maxCoverDistance = graph.getArgMaxNodeDistance(c)
                    break
                
                add = True
                for v in seeds:
                    if(graph.getValue(c,v) < maxCoverDistance/5):                   
                        add = False
                    if(c in seeds):
                        add = False
                        continue

                if(add == True): 
                    if(len(seeds)< n_vehicles):      
                        seeds.append(c)
                        scannerRadius[c] = 0
                        #depotDistance[c] = 0
                        maxCoverDistance = graph.getArgMaxNodeDistance(c)
                        break
                else:
                    if ( sum(demand) == dimension-1):
                        if(c in seeds):
                            continue
                        else:
                            scannerRadius[c] = 0
                            #depotDistance[c] = 0
                            continue

        if ( sum(demand) != dimension-1):
            print("Decrease Radious")
            scannerRadius[np.argmax(scannerRadius)] = 0

                    
        scaledown = scaledown + 0.5
        print(np.max(scannerRadius))

    count = []
    fromCenter = []
    for s in seeds:
        fromCenter.append(appo[s])
        for v in seeds:
            if s!=v:
                count.append(graph.getValue(s,v))
            


    if ( sum(demand) != dimension-1):
            print("\n")
            print("Seeds demand: ")
            [print(str(demand[s]), end=" - ") for s in seeds]
            print('\n')
            print("Graph Demand Distribution ==> Max : " + str(np.max(demand)) +" Min : " + str(np.min(demand[1:])))
            print('\n')
    print("Seeds Inter Distance      ==> Max : " + str(np.max(count)) +" Min : " + str(np.min(count)))
    print("Graph Distribution        ==> Max : " + str(graph.getMaxInterNodesDistance()) +" Min : " + str(graph.getMinInterNodesDistance()))

    print("Seeds Depot Distance      ==> Max : " + str(np.max(fromCenter)) +" Min : " + str(np.min(fromCenter)))
    print("Node-Depot  Distance      ==> Max : " + str(np.max(appo)) +" Min : " + str(np.min(appo[1:])))


    print("Done")
    print("==========================================================================================")

    return seeds

def GAPsolver(graph,k_clusters):

    dimension = graph.getDimension()
    n_cluster = len(k_clusters)
    capacity = graph.getCapacity()
    demand = graph.getDemand()
    # depot = graph.getDepot()
    allocCosts =   np.zeros(shape=(dimension, n_cluster))
    clusterAssignment = []
    cluster_demand = np.zeros(n_cluster)
 
    for i in range(1,dimension):
        for k in k_clusters:
            a =  graph.getValue(0,i)+ graph.getValue(i,k)+graph.getValue(k,0)
            b =  graph.getValue(0,k)+ graph.getValue(k,i)+graph.getValue(i,0)
            a_ik = min(a,b) - (graph.getValue(0,k) + graph.getValue(k,0))
            allocCosts[i][k_clusters.index(k)] = a_ik
    
    i = 1
    for alloc in allocCosts[1:]:
        for k  in k_clusters:
                if(cluster_demand[np.argmin(alloc)] + demand[i] < capacity):
                    cluster_demand[np.argmin(alloc)] += demand[i]
                    clusterAssignment.append(np.argmin(alloc))
                    i=i+1
                    break
                else:
                    alloc[np.argmin(alloc)] = np.inf
                    print("Cluster Overloaded")

        #Devo tenere conto che la capacità di un cluster non deve eccedere
        #Ok, ma se i cluster non bastano? Se le route sono 6 ma i cluster sono 5?
    if(len(clusterAssignment)<graph.getDimension()-1):
        print("Solution is Invalid")
        return -1
    else:
        return clusterAssignment

def FisherJaikumar_Routing(graph,clusterAssignment,k_clusters,saveFolder):

    routes = []
    capacity = graph.getCapacity()
    demand = graph.getDemand()
    depot = graph.getDepot()

    for k in range(len(k_clusters)):
        cluster = []
        for i in range(len(clusterAssignment)):
            if(clusterAssignment[i] == k ):
                cluster.append(i+1)
        
       
        appoRoute =  Route(graph.getCapacity()) 
        appoRoute.addCustomer(0,0,False)

        while(len(cluster)>0):
            prevnode = appoRoute.getCustomers()[len(appoRoute.getCustomers())-1]
            distPrevNode = graph.getValue(prevnode,[c for c in cluster if c not in appoRoute.getCustomers() ])
            nearestN = cluster[np.argmin(distPrevNode)] 
            if nearestN not in appoRoute.getCustomers():
                appoRoute.addCustomer(nearestN,demand[nearestN],False)
                cluster.remove(nearestN)
    
        appoRoute.addCustomer(0,0,False)
        appoRoute.printRoute("Route cluster:" +str(k))
        routes.append(appoRoute)

    
    totSolCost = 0
    routedNodesControl = 1
    f= open(saveFolder +"/Sol_"+graph.getFileName()+".txt","w+")
    f.write(str(graph.name)+"\n")
    f.write(str(graph.dimension)+"\n")
    
    for fianlRoute in routes:
        routeCost = 0    
        appo = fianlRoute.printRoute(routes.index(fianlRoute))
        f.write(appo+"\n")
        for i in range(len(fianlRoute.getCustomers())-1):
            routedNodesControl = routedNodesControl +1
            routeCost += graph.getValue(fianlRoute.getCustomers()[i], fianlRoute.getCustomers()[i+1])
        routedNodesControl = routedNodesControl -1
        fianlRoute.setCost(routeCost)
        totSolCost += routeCost

    if(routedNodesControl < graph.getDimension()):
        print("No solution")
    f.write("Total Routed Nodes "+ str(routedNodesControl)+"\n")
    f.write("Routing Total Cost: "+ str(totSolCost)+"\n")
    print("Routing Total Cost: "+ str(totSolCost)+"\n")
    
    return routes

def FisherJaikumar_Routing_Dijkastra(graph,clusterAssignment,k_clusters,saveFolder):

    finalRoutes = []
    capacity = graph.getCapacity()
    demand = graph.getDemand()
    depot = graph.getDepot()
    dimension = graph.getDimension()
    dist = np.zeros(dimension)
    priorityQ =[]
    
    for k in range(len(k_clusters)):
        cluster = []
        routes =[]
        for i in range(len(clusterAssignment)):
            if(clusterAssignment[i] == k ):
                cluster.append(i+1)

        if len(cluster) < 1 :
            continue

        for node in cluster:          
            nodeRoute = Route(graph.getCapacity())
            nodeRoute.addCustomer(0,demand[0],False)
            nodeRoute.addCustomer(node,demand[node],False)
            nodeRoute.setCost(graph.getValue(0,node))
            priorityQ.append(nodeRoute)
        
        priorityQ.sort(key=lambda x: x.getCost(),reverse=True)
        
        while len(priorityQ) > 0 :
            shortRoute = priorityQ.pop()
          
            prevNode = shortRoute.getCustomers()[len(shortRoute.getCustomers())-1]
            appoCluster = []
            for v in cluster:
                if v!= prevNode:
                    if(shortRoute.checkCustomer(v) == -1):
                        appoCluster.append(v)
            if len(appoCluster) > 0:
                index,value = graph.getNearestNeighbours(prevNode,appoCluster)
                costToAdd = shortRoute.getCost() + value
                shortRoute.setCost(costToAdd)
                shortRoute.addCustomer(appoCluster[index],demand[appoCluster[index]],False)
                priorityQ.append(shortRoute)
                priorityQ.sort(key=lambda x: x.getCost(),reverse=True)
            else:
                value = graph.getValue(prevNode,0)
                costToAdd = shortRoute.getCost() + value
                shortRoute.setCost(costToAdd)
                shortRoute.addCustomer(0,0,False)               
                routes.append(shortRoute)


      
     
  
        print("Areo")
        routes.sort(key=lambda x: x.getCost(),reverse=True)
        #a = np.argmin([r.getCost() for r in routes])
        route = routes.pop()
        route.printRoute("Route")

        finalRoutes.append(route)
    
    totSolCost =  0
    routeCost = 0  
    routedNodesControl = 1
    f= open(saveFolder+'/Sol_'+graph.getFileName()+".txt","w+")
    f.write(str(graph.name)+"\n")
    f.write(str(graph.dimension)+"\n")
    
    for fianlRoute in finalRoutes:
        
        appo = fianlRoute.printRoute(finalRoutes.index(fianlRoute))
        routeCost = 0
        f.write(appo+"\n")
        for i in range(len(fianlRoute.getCustomers())-1):
            routedNodesControl = routedNodesControl +1
            routeCost += graph.getValue(fianlRoute.getCustomers()[i], fianlRoute.getCustomers()[i+1])
        routedNodesControl = routedNodesControl -1
        fianlRoute.setCost(routeCost)
        totSolCost += routeCost
    f.write("Total Routed Nodes "+ str(routedNodesControl)+"\n")
    f.write("Routing Total Cost: "+ str(totSolCost)+"\n")

    return finalRoutes

def ClusterFirst_RouteSecond(graph,saveFolder):

    finalRoutes = []
    capacity = graph.getCapacity()
    demand = graph.getDemand()
    depot = graph.getDepot()
    dimension = graph.getDimension()
    dist = [np.inf for i in range(dimension)]
    nodeQueue= []
    auxGraph = [(i,Route(capacity)) for i in range(dimension)]
    
  

    #Source Node has 0 cost, in this case route Depot - 1- Depot
    dist[0] = 0

    #nodeQueue = [(c+1,dist[c]) for c in range(len(dist))]
    route = Route(capacity)
    route.addCustomer(0,demand[0],False)
    route.addCustomer(1,demand[1],False)
    route.addCustomer(0,demand[0],False)
    route.setCost(0)

    nodeQueue = [(1,0,route)]
    node = 0
    nodeQueue.sort(key=lambda x: x[1],reverse=True)

    while len(nodeQueue)>0:
        #Give the node in the auxiliary graph that has low cost
        nodeToexpand = nodeQueue.pop()
        node = nodeToexpand[0]
        cost = nodeToexpand[1]
        prevRoute =nodeToexpand[2] 
        #Give the corresponding route, that contain node
        #auxGraph.pop()
        #Create each child of the node in the auxiliary graph
        for j in range(1,dimension):
            #j child
            if(j >= node):
                newRoute = Route(capacity)
                newRoute.setCost(0)
                newRoute.addCustomer(0,demand[0],False)
                control = -3
                #for each child that not exceed the truck capacity
                for i in range(node,j+1):
                    #The not is not in the route and it not exceed the truck capacity
                    #Add Node
                    if (newRoute.checkCustomer(i) == -1):
                        control = newRoute.addCustomer(i,demand[i],False)
                        #Update Cost
                        if(control > 0):
                            newRoute.setCost(newRoute.getCost() + graph.getValue(newRoute.getCustomers()[node-i],i))
                        else:                            
                            break
                #Close the route 
                if(control > 0):
                    newRoute.setCost(newRoute.getCost() + graph.getValue(j,0))
                    newRoute.addCustomer(0,demand[0],False)
                    if(dist[j] > newRoute.getCost()+ cost):
                        dist[j] = newRoute.getCost() +cost
                        nodeQueue.append((j+1,dist[j],newRoute))
                        auxGraph[j] = (node-1,newRoute)
                        nodeQueue.sort(key=lambda x: x[1],reverse=True)
                else: break
    

    u = len(auxGraph)-1
    while (u != 0):
        node = auxGraph[u]
        u = node[0]
        finalRoutes.append(node[1])
        
    routeCost = 0  
    routedNodesControl = 1
    f= open(saveFolder+'/Sol_'+graph.getFileName()+".txt","w+")
    f.write(str(graph.name)+"\n")
    f.write(str(graph.dimension)+"\n")
    
    for fianlRoute in finalRoutes:
            
        appo = fianlRoute.printRoute(finalRoutes.index(fianlRoute))
        f.write(appo+"\n")
        for i in range(len(fianlRoute.getCustomers())-1):
            routedNodesControl = routedNodesControl +1
            routeCost += graph.getValue(fianlRoute.getCustomers()[i], fianlRoute.getCustomers()[i+1])
        routedNodesControl = routedNodesControl -1
    
    f.write("Total Routed Nodes "+ str(routedNodesControl)+"\n")
    f.write("Routing Total Cost: "+ str(routeCost)+"\n")


def LocalSearch_FlippingPath(route:Route,graph:cvrpGraph,candidate1, candidate2):

    node1 = candidate1 % len(route.getCustomers())
    node2 = candidate2 % len(route.getCustomers())
    if(node2 != 0):
        firstCandidate = route.getCustomers()[node1] 
        prevfc =  route.getCustomers()[node1-1] 
        nextfc =  route.getCustomers()[node1+1]

        secondCandidate = route.getCustomers()[node2]
        prevsc =  route.getCustomers()[node2-1] 
        nextsc =  route.getCustomers()[node2+1]

        cost1 = graph.getValue(prevfc,firstCandidate) + graph.getValue(firstCandidate,nextfc)
        cost2 = graph.getValue(prevsc,secondCandidate) + graph.getValue(secondCandidate,nextsc)

        route.setCost (route.getCost() - (cost1 +cost2))
        route.getCustomers()[firstCandidate] = secondCandidate
        route.getCustomers()[secondCandidate] = firstCandidate

        cost3 = graph.getValue(prevfc,secondCandidate) + graph.getValue(secondCandidate,nextfc)
        cost4 = graph.getValue(prevsc,firstCandidate) + graph.getValue(firstCandidate,nextsc)

        route.setCost (route.getCost() + (cost3 +cost4))
           
    return route

def Mutation(children,graph:cvrpGraph,percentage:int):

    mutant = []
    demand = graph.getDemand()
    for child in children:
        candidates = []
        toSubstitute = []

        n_nodes = math.ceil((len(child.getCustomers()) * percentage) / 100)

        candidates = [np.random.randint(1,graph.getDimension()) for i in range(n_nodes)]

        if(len(child.getCustomers()) ==2 ):
            continue
        else:
            toSubstitute = [np.random.randint(1,len(child.getCustomers())-1) for i in range(n_nodes)]

        for i in range(len(candidates)):
            j = toSubstitute[i]
            nodeTosub = child.getCustomers()[j]
            if(child.getPayload() + demand[candidates[i]] - demand[nodeTosub] <= child.getCapacity()):
                c = child.getCustomers().index(nodeTosub)
                prevc =  child.getCustomers()[c-1] 
                nextc =  child.getCustomers()[c+1]

                costDel = graph.getValue(prevc,c) + graph.getValue(c,nextc)
                child.setCost (child.getCost() - (costDel))
        
                d = candidates[i]
                indexBefore =  child.getCustomers().index(nodeTosub)  
                child.getCustomers().insert(indexBefore+1,d)
                child.getCustomers().remove(nodeTosub)
                costToAdd = graph.getValue(prevc,d) + graph.getValue(d,nextc)
                child.setCost (child.getCost() + costToAdd)
                mutant.append(child)
            else: 
                mutant.append(child)
                continue

    return mutant


def Elitism(population): 
    #toCopy = math.ceil((len(chromosome) * elitism_precentage / 100))
    populSort = population.copy()
    populSort.sort(key= lambda x:x[0],reverse=True)
    toKeep = populSort.pop()
    return toKeep

def Tournament(population,random:bool):

    if(random == True):
        c1 = np.random.randint(len(population))
        c2 = np.random.randint(len(population))
        f1,winner1 = population[c1]
        f2,winner2 = population[c2]
        return winner1,winner2,f1,f2

    winners = population.copy()
    winners.sort(key=lambda x:x[0],reverse=True)
    f1,w1 = winners.pop()
    f2,w2 = winners.pop()
    return w1, w2,f1,f2
    # winner = [ (f.getCost()/len(f.getCustomers()),f) for f in fitness  ]
    # winner.sort(key=lambda x:x[0])
    # if(best == True):
    #     winner = winner[:int(len(winner)/2)]
    # else:
    #     winner = winner[int(len(winner)/2):]
    # return winner

    
def Crossover(winner1,winner2,graph:cvrpGraph,tabuSearch:bool = False,tabuLister:list = []):

    demand = graph.getDemand()
    capacity = graph.getCapacity()
    tabuList = tabuLister
    ft = Route(capacity)    
    winner1Sequence = []
    winner2Sequence = []

    child1 = []
    child2 = []
    solution1 = []
    solution2 = []

    winner1Sequence += [p.getCustomers() for p in winner1]
    winner1Sequence = [y for x in winner1Sequence for y in x if y!=0]
    winner2Sequence += [p.getCustomers() for p in winner2]
    winner2Sequence = [y for x in winner2Sequence for y in x if y!=0]

    #winner1Sequence = [1 ,2 ,3 , 5 ,4 ,6 ,7 , 8 ,9]
    #winner2Sequence = [4 ,5 ,2 , 1 ,8, 7 ,6 , 9 ,3]


    crossover_point1 = np.random.randint(int(len(winner1Sequence)/4),(int(len(winner1Sequence)/2)))
    crossover_point2 = np.random.randint(int(len(winner1Sequence)/2),(int(len(winner1Sequence)/2) +int(len(winner1Sequence)/4)))

    #Form child one List
    for node in (winner1Sequence[crossover_point1:crossover_point2]):
        if node not in child1 and node !=0:
            child1.append(node)
    
    for node in (winner2Sequence[crossover_point2:]):
        if node not in child1 and node !=0:
            child1.append(node)

    for node in (winner2Sequence[:crossover_point2]):
       if node not in child1 and node !=0:
            child1.insert(0,node)
    
    #Build and check the child one Route
    
    i=0
    while(i < len(child1)):
        route = Route(capacity)
        cost = 0
        route.setCost(0)
        route.addCustomer(0,demand[0],False)
        for node in child1[i:]:
            i =i+1
            if(route.addCustomer(node,demand[node],False)<0):
                if(route.checkCustomer(node)== -1):
                    route.addCustomer(0,demand[0],False)
                    i = i-1
                break
            if(len(child1) == i ):
                route.addCustomer(0,demand[0],False)
        for n in range(len(route.getCustomers())-1):
            cost += graph.getValue(route.getCustomers()[n],route.getCustomers()[n+1])
        route.setCost(cost)
        solution1.append(route)
    


   #Form child two  List
    for node2 in (winner2Sequence[crossover_point1:crossover_point2]):
        if node2 not in child2 and node2 !=0:
            child2.append(node2)
    
    for node2 in (winner1Sequence[crossover_point2:]):
        if node2 not in child2 and node2 !=0:
            child2.append(node2)

    for node2 in (winner1Sequence[:crossover_point2]):
       if node2 not in child2 and node2 !=0:
            child2.append(node2)
    
     

    
    #Build and check the child one Route
    
    i=0
    while(i < len(child2)):
        route2 = Route(capacity)
        cost = 0
        route2.setCost(0)
        route2.addCustomer(0,demand[0],True)
        for node in child2[i:]:
            i = i+1
            if(route2.addCustomer(node,demand[node],False)<0):
                route2.addCustomer(0,demand[0],False)
                i = i-1
                break
        if(len(child2) == i ):
                route2.addCustomer(0,demand[0],False)
        for n in range(len(route2.getCustomers())-1):
            cost += graph.getValue(route2.getCustomers()[n],route2.getCustomers()[n+1])
        route2.setCost(cost)
        solution2.append(route2)

    
    f1 = sum([c.getCost() for c in solution1])
    f2 = sum([c.getCost() for c in solution2])

    tabuState = []
    if(f1> f2):
        tabuState = f1
    else: 
        tabuState = f2

    if(tabuSearch == True and int(tabuState) in tabuList):
            print("TABULISTED ==> " +str(int(tabuState))) 
            return Crossover(winner1,winner2,graph,tabuList)
    else:            
        tabuList.append(int(tabuState))

    if(f1<f2): 
        return solution1,tabuList,f1
    else:
        return solution2,tabuList,f2


def SearchaAndCompleteSequence(solution:[Route],graph:cvrpGraph):

    nodes = []
    nodesToCheck = [ i for i in range(1,graph.getDimension())]
    
    for route in solution:                   
        for n in route.getCustomers():
            if(n!=0):
                if n not in nodes:
                    nodes.append(n)
                    nodesToCheck.remove(n)
        
    if (len(nodesToCheck)>0 and len(nodes)!= graph.getDimension() -1): 
        return True 
    else: 
        return False
    

   
        

            


         





    
    


        



    





        



    

    
    
