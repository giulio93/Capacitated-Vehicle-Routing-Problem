import numpy as np
from cvrpGraph import cvrpGraph
import operator
from route import Route


def ClarkeWright(graph,demand):
    print("Clarke & Wright have been evoked!")

    dimension = graph.getDimension()

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
            r.addCustomer(i,demand[i],False)
            r.addCustomer(j,demand[i],False)

        


    print("a")


    
    
