import numpy as np
from cvrpGraph import cvrpGraph
import operator
from route import Route


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
                    if(graph.getValue(c,v) < maxCoverDistance/3):                   
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

def FisherJaikumar_GAPSolver(graph,k_clusters):

    dimension = graph.getDimension()
    n_cluster = len(k_clusters)
    # capacity = graph.getCapacity()
    # demand = graph.getDemand()
    # depot = graph.getDepot()
    allocCosts =   np.zeros(shape=(dimension, n_cluster))
    clusterAssignment = []
 
    for i in range(1,dimension):
        for k in k_clusters:
           a =  graph.getValue(0,i)+ graph.getValue(i,k)+graph.getValue(k,0)
           b =  graph.getValue(0,k)+ graph.getValue(k,i)+graph.getValue(i,0)
           a_ik = min(a,b) - (graph.getValue(0,k) + graph.getValue(k,0))
           allocCosts[i][k_clusters.index(k)] = a_ik
    
    for alloc in allocCosts:
        clusterAssignment.append(np.argmin(alloc))
        #Devo tenere conto che la capacità di un cluster non deve eccedere
        #Ok, ma se i cluster non bastano? Se le route sono 6 ma i cluster sono 5?

    return clusterAssignment

def FisherJaikumar_Routing(graph,clusterAssignment,k_clusters):

    routes = []
    capacity = graph.getCapacity()
    demand = graph.getDemand()
    depot = graph.getDepot()
    for k in k_clusters:
        cluster = []
        for ca in  clusterAssignment:
            if(ca == k ):
                cluster.append(clusterAssignment.index(ca))

    for x in (cluster):
        appoRoute =  Route(graph.getCapacity()) 
        appoRoute.addCustomer(x,demand[x],False)
        routes.append(appoRoute)
        



    





        



    

    
    
