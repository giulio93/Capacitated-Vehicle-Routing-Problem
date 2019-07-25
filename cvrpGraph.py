# coding: utf-8

import numpy as np


class cvrpGraph:

    def __init__(self):
        self.name = None
        self.filename = None
        self.dimension = 0
        self.adjMatrix = None  # The graph is modeled with a matrix
        self.capacity = None  #  The loading capacity setted by the cvrp files
        self.comment = None
        self.demand = []
        self.depot = []
        

    def setCapacity(self, capacity):
        self.capacity = capacity

    def getCapacity(self):
        return self.capacity

    def setComment(self, comment):
        self.comment = comment

    def getComment(self, comment):
        self.comment = comment

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name
    
    def setFileName(self, filename):
        self.filename = filename

    def getFileName(self):
        return self.filename

    def getValue(self, i, j):  
        return self.adjMatrix[i][j]

    def setDimension(self, dimension):
        self.dimension = dimension
        self.adjMatrix = np.zeros(shape=(self.dimension, self.dimension))

    def getDimension(self):
        return self.dimension

    def addEdge(self, vertex_from, vertex_to, weight):
        self.adjMatrix[vertex_from][vertex_to] = weight
        self.adjMatrix[vertex_to][vertex_from] = weight

    def setDemand(self,demand):
        self.demand = demand
        
    def getDemand(self):
        return self.demand

    def setDepot(self,depot):
        self.depot = depot
        
    def getDepot(self):
        return self.depot


