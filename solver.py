import numpy as np
from cvrpGraph import cvrpGraph


def ClarkeWright(graph):
    print("Clarke & Wright have been evoked!")

    dimension = graph.getDimension()

    savings = [dimension,dimension]
    for i in range(dimension):
        for j in range(dimension):
            save = graph.getValue(i,0) + graph.getValue(0,j) - graph.getValue(i-j)
            savings[i,j] = save


    
    
