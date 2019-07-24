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
    for save in savings:
        i = save[1]
        j = save[2]
        customerI = -1
        customerJ = -1
        routeA = -1
        routeB = -1

        # no routes have been created yet
        if len(routes) == 0:
            r =  Route(graph.getCapacity())
            r.addCustomer(i,demand[i],True)
            r.addCustomer(j,demand[i],False)
            routes.append(r)
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
                r =  Route(graph.getCapacity())
                control1 =  r.addCustomer(i,demand[i],False)
                control2 =  r.addCustomer(j,demand[j],False)
                # No constraint violated on the route
                if(control1 != -1 and control2 != -1):
                    routes.append(r)
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
                            
        #filize routing adding connection to the Depot
    for r in routes:
        r.addCustomer(0,0,True)
        r.addCustomer(0,0,False)
        r.printRoute()



    

    
    
