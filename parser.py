import pandas as pd
import os
import numpy as np
from cvrpGraph import cvrpGraph
from math import acos, cos, sqrt, pi
import math


def readInstanceList(path):
    files = os.listdir(path)
    return files


def createGraph(folderRoot,fileCVRP):

    g = cvrpGraph()
    g.setFileName(fileCVRP)
    data = pd.read_csv(folderRoot+'/'+fileCVRP, sep="\n", header=None)
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
                print("Comment: " + (line[1])+line[3].split(',')[0]+')')
                g.setComment(line[1]+line[3].split(',')[0]+')')

            if line[0] == "TYPE":
                if "CVRP" != line[1].strip():
                    print(
                        "Your input data are not suitable for this algo, please input a TSP format")

            if line[0] == "DIMENSION":
                dimension = int(line[1].strip()) 
                g.setDimension(dimension)
                print("Dimension: " + str(dimension))

            if line[0] == "EDGE_WEIGHT_TYPE":
                w_type = (line[1]).strip()

            if line[0] == "EDGE_WEIGHT_FORMAT":
                w_format = (line[1]).strip()

            if line[0] == "NODE_COORD_TYPE":
                n_c_type = (line[1]).strip()
            
            if line[0] == "DEMAND_SECTION":
                initDemand(g,data,i+1)
            
            if line[0] == "DEPOT_SECTION":
                initDepot(g,data,i+1)

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
    return g


def initDemand(graph,data,index):
    
    dimension = graph.getDimension()
    appoDemand = np.zeros(dimension)
    while data[0][index].strip() != "DEPOT_SECTION":

        toSplit = data[0][index].split()
        appoDemand[int((toSplit[0]))-1] += int((toSplit[1]))
        index += 1

    graph.setDemand(appoDemand)

def initDepot(graph,data,index):
    
    dimension = graph.getDimension()
    appoDepot = np.repeat(-1,dimension)
    while data[0][index].strip() != '-1':

        depot = int(data[0][index])
        appoDepot[depot-1] += depot
        index += 1

    graph.setDepot(appoDepot)

def parseEUC2 (graph, data, index):

    dimension = graph.getDimension()
    appoVertex = dict()

    while len(data[0][index].split()) > 1:

        toSplit = data[0][index].split()
        appoVertex[int((toSplit[0]))] = [(toSplit[1]), (toSplit[2])]
        index += 1

    for i in range(dimension):
        a = appoVertex[i+1]
        for j in range(dimension):
            if i != j:             
                b = appoVertex[j+1]
                weight = np.sqrt(((float(a[0]) - float(b[0]))**2) + ((float(a[1]) - float(b[1]))**2))
                graph.addEdge(i,j, weight)



    print("EUC2  Done")
       


def parseGEO(graph,data, index):

    dimension = graph.getDimension()
    appoVertex = dict()
    PI = 3.141592

    while len(data[0][index].split()) > 1:

        toSplit = data[0][index].split()
        appoVertex[int((toSplit[0]))] = [float((toSplit[1])),float((toSplit[2]))]
        index += 1

    for i in range(dimension):
        a = appoVertex[i+1]
        degrees = int(math.ceil(a[0]))
        minutes = a[0] - degrees
        latitudeA = PI * (degrees + 0.5 * minutes / 0.3) / 180.0
        degrees = int(a[1])
        minutes = a[1] - degrees
        longitudeA = PI * (degrees + 0.5 * minutes / 0.3) / 180.0
        for j in range(dimension):
            if i!=j:
                b = appoVertex[j+1]
                degrees = int(math.ceil(b[0]))
                minutes = b[0] - degrees
                latitudeB = PI * (degrees + 0.5 * minutes / 0.3) / 180.0
                degrees = int(a[1])
                minutes = b[1] - degrees
                longitudeB = PI * (degrees + 0.5 * minutes / 0.3) / 180.0                     
                RRR = 6378.388
                q1 = np.cos(longitudeA - longitudeB)
                q2 = np.cos(latitudeA - latitudeB)
                q3 = np.cos(latitudeA + latitudeB)
                dij = int(RRR * acos(0.5 * ((0.1 + q1) * q2 - (1.0 - q1) * q3)) +1.0)
                graph.addEdge(i, j, dij)
            else:  graph.addEdge(i, j, -1)



def parseMatrix(graph, format, data,index):

    dimension = graph.getDimension()
    appoMatrix = []

    while (data[0][index].split()[0].strip() != ("DEMAND_SECTION") 
            and data[0][index].split()[0].strip() != ("DISPLAY_DATA_SECTION")):
        
        row = data[0][index]
        appoMatrix += ([float(weight) for weight in row.split()])
        index += 1

    appoMatrix = np.array(appoMatrix)
    graphMatrix = np.zeros((dimension, dimension))
    if format == "FULL_MATRIX":
        graphMatrix = appoMatrix.reshape((dimension, dimension))

    elif format == "LOWER_DIAG_ROW":
        indices = np.tril_indices(dimension)       
        graphMatrix[indices] = appoMatrix

    elif format == "UPPER_ROW":
        indices = np.triu_indices(dimension, 1)
        indices2 = np.tril_indices(dimension,-1)    
        graphMatrix[indices] = appoMatrix
        graphMatrix[indices2] = appoMatrix

    if format != "FULL_MATRIX":
        for i in range(dimension):
            for j in range(dimension):
                graph.addEdge(i, j, float(graphMatrix[i][j]))


    else:
        for i in range(dimension):
            for j in range(dimension):
                graph.addEdge(i, j, float(graphMatrix[i][j]))
               

    
    print("Done")



