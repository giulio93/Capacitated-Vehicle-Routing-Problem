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

        if len(routes) == 0:
            r =  Route(graph.getCapacity())
            r.addCustomer(i,demand[i],True)
            r.addCustomer(j,demand[i],False)
            routes.append(r)
        else:
            for route in routes:
                customerI = route.checkCustomer(i)
                customerJ = route.checkCustomer(j)

            if(customerI == -1  and customerJ == -1):
                r =  Route(graph.getCapacity())
                control =  r.addCustomer(i,demand[i],False)
                control =  r.addCustomer(j,demand[i],False)
                if(control != -1):
                    routes.append(Route(r))
            
            if (customerI != -1 and customerJ == -1):
                if(customerI == 0):
                    route.addCustomer(j,demand[j],True)
                else:
                    route.addCustomer(j,demand[j],False)

            if (customerI == -1 and customerJ != -1):
                if(customerJ == 0):
                  route.addCustomer(i,demand[i],True)
                else:
                  route.addCustomer(i,demand[i],False)

    for r in routes:
        r.addCustomer(0,0,True)
        r.addCustomer(0,0,False)
        r.printRoute()



    

    
    
