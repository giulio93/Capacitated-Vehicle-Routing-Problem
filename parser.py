import pandas as pd
import os
import numpy as np
from cvrpGraph import cvrpGraph
from GraphAdjList import Graph


def readInstanceList(path):
    files = os.listdir(path)
    return files


def createGraph(files):

    g = cvrpGraph()
    for f in files:
        data = pd.read_csv('cvrp/'+f, sep="\n", header=None)
        i = 0
        for d in data[0]:
            line = d.split(':')
            line[0] = line[0].strip()
            if line[0] == "NAME":
                print("Instance Name: "+ (line[1]))
                g.setName(line[1].strip())
            if line[0] == "CAPACITY":
                print("Vehicle Capacity: " + (line[1]))
                g.setCapacity(int(line[1].strip()))
            if line[0] == "COMMENT":
                print("Comment: " + (line[1]))
                g.setComment(line[1])
            if line[0] == "TYPE":
                if "CVRP" != line[1]:
                    print(
                        "Your input data are not suitable for this algo, please input a TSP format")
            if line[0] == "DIMENSION":
                dimension = int(line[1]) -1
                g.setDimension(int(line[1].strip()))
                print("Dimension: " + str(dimension))
            if line[0] == "EDGE_WEIGHT_TYPE":
                w_type = (line[1]).strip()

            if line[0] == "EDGE_WEIGHT_FORMAT":
                w_format = (line[1]).strip()

            if line[0] == "NODE_COORD_TYPE":
                n_c_type = (line[1]).strip()

            if line[0] == "NODE_COORD_SECTION":
                if w_type == "EUC_2D":
                    print("Edge are expressed: " + w_type)
                    parseEUC2(g, data, i+1)
                if w_type == "GEO":
                    print("Edge are expressed: " + w_type)
                    parseGEO(g, data ,i+1)
            if line[0] == "EDGE_WEIGHT_SECTION":
                if w_type == "EXPLICIT":
                    print("Edge are expressed:" + w_type)
                    parseMatrix(g, w_format, data,i+1)
            if line[0] == "EOF":
                print("============================================================================")
                break
            i += 1


def parseEUC2 (graph, data, index):

    dimension = graph.getDimension()
    appoVertex = dict()

    while len(data[0][index+1].split()) > 1:

        toSplit = data[0][index].split()
        appoVertex[int((toSplit[0]))] = [(toSplit[1]), (toSplit[2])]
        index += 1

    for i in range(dimension-1):
        a = appoVertex[i+1]
        for j in range(dimension-1):
            if i != j:             
                b = appoVertex[j+1]
                weight = np.sqrt(((float(a[0]) - float(b[0]))**2) + ((float(a[1]) - float(b[1]))**2))
                graph.addEdge(i,j, weight)

    print("EUC2  Done")
       


def parseGEO(graph,data, index):

    dimension = graph.getDimension()
    appoVertex = dict()

    while len(data[0][index+1].split()) > 1:

        toSplit = data[0][index].split()
        appoVertex[int((toSplit[0]))] = [(toSplit[1]), (toSplit[2])]
        index += 1

    for i in range(dimension-1):
        a = appoVertex[i+1]
        degrees = int(float(a[0]))
        minutes = float(a[0]) - degrees
        latitudeA = np.pi * (degrees + 0.5 * minutes / 0.3) / 180.0
        degrees = int(float(a[1]))
        minutes = float(a[1]) - degrees
        longitudeA = np.pi * (degrees + 0.5 * minutes / 0.3) / 180.0
        for j in range(dimension-1):
            if i != j:
                b = appoVertex[j+1]
                degrees = int(float(b[0]))
                minutes = float(b[0]) - degrees
                latitudeB = np.pi * (degrees + 0.5 * minutes / 0.3) / 180.0
                degrees = int(float(a[1]))
                minutes = float(b[1]) - degrees
                longitudeB = np.pi * (degrees + 0.5 * minutes / 0.3) / 180.0                     
                RRR = 6378.388
                q1 = np.cos(longitudeA - longitudeB)
                q2 = np.cos(latitudeA - latitudeB)
                q3 = np.cos(latitudeA + latitudeB)
                dij = int(RRR * np.arccos(0.5 * ((0.1 + q1) * q2 - (1.0 - q1) * q3)) +1.0)
                graph.addEdge(i, j, dij)



def parseMatrix(graph, format, data,index):

    dimension = graph.getDimension()
    matrix_temp = []

    for d in data[0]:
        line = d.split()
        keyword = line[1]
        if keyword == "DEMAND_SECTION" or keyword == "DISPLAY_DATA_SECTION":
            break
        row = [float(el) for el in line.split()]
        matrix_temp += row
    # matrix_temp = np.array(matrix_temp)
    # matrix = np.zeros((dimension, dimension))
    # if format == "FULL_MATRIX":
    #     matrix = matrix_temp.reshape((dimension, dimension))

    # elif format == "LOWER_DIAG_ROW":
    #     indices = np.tril_indices(dimension)
    #     matrix[indices] = matrix_temp

    # elif format == "UPPER_ROW":
    #     indices = np.triu_indices(dimension, 1)
    #     matrix[indices] = matrix_temp

    # for i in range(dimension):
    #     for j in range(dimension):
    #         graph.add_edge(i, j, float(matrix[i][j]))

