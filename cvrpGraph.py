# coding: utf-8

import numpy as np


class cvrpGraph:

    def __init__(self):
        self.name = None
        self.dimension = 0
        self.adjMatrix = None # The graph is modeled with a matrix
        self.capacity = None  # The loading capacity setted by the cvrp files
        self.comment = None

    def setCapacity(self, capacity):
        self.capacity = capacity

    def getCapacity(self):
        return self.capacity

    def setComment(self,comment):
        self.comment = comment
        
    def getComment(self,comment):
        self.comment = comment

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def getValue(self, i, j):  # TODO cambia nome
        return self.adjMatrix[i][j]

    def setDimension(self, dimension):
        self.dimension = dimension
        self.adjMatrix = np.zeros(shape=(self.dimension, self.dimension))

    def getDimension(self):
        return self.dimension

    def addEdge(self, vertex_from, vertex_to, weight):
        self.adjMatrix[vertex_from][vertex_to] = weight
        self.adjMatrix[vertex_to][vertex_from] = weight





