# coding: utf-8

import numpy as np
import networkx as nx
import random


class Graph:

    def __init__(self, graph_dict=None):
        if graph_dict == None:
            graph_dict = {}
        self.__graph_dict = graph_dict

    def vertices(self):
        """ returns the vertices of a graph """
        return list(self.__graph_dict.keys())

    def edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()

    def add_vertex(self, vertex):
        """ If the vertex "vertex" is not in
            self.__graph_dict, a key "vertex" with an empty
            list as a value is added to the dictionary.
            Otherwise nothing has to be done.
        """
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []

    def add_edge(self, edge):
        """ assumes that edge is of type set, tuple or list; 
            between two vertices can be multiple edges! 
        """
        edge = set(edge)
        if(len(edge) == 1):
            elem = edge.pop()
            if elem in self.__graph_dict.keys():
                self.__graph_dict[elem].append(elem)
            else:
                self.__graph_dict[elem] = []

        elif (len(edge) > 1):
            (vertex1, vertex2) = tuple(edge)
            if vertex1 in self.__graph_dict.keys():
                self.__graph_dict[vertex1].append(vertex2)
            else:
                self.__graph_dict[vertex1] = []

        else:
            print("out")

    def __generate_edges(self):
        """ A static method generating the edges of the 
            graph "graph". Edges are represented as sets 
            with one (a loop back to the vertex) or two 
            vertices 
        """
        edges = []
        counter = 0
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                counter += 1
                if({vertex, neighbour} not in edges):
                    edges.append({vertex, neighbour})
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self.__graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res

    def ER(self, n, p):
       # Directed Graph.
        ErReGraph = nx.DiGraph()
        appoGraph = Graph()

        # ER Algorithm.
        for n1 in range(n):
            for n2 in range(n):
                a = random.uniform(0.0, 1.0)
                if a < p and n1 != n2:
                    appoGraph.add_edge({n1, n2})
                    ErReGraph.add_edge(n1, n2)

        print("Vertices of graph:")
        print(len(appoGraph.vertices()))

        print("Edges of graph:")
        print(len(appoGraph.edges()))

        print("Number of edges: ", len(ErReGraph.edges()))
        print("Number of nodes: ", len(ErReGraph.nodes()))
        return appoGraph
