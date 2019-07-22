# coding: utf-8

import os
import parser as par
import solver as sol

if __name__ == "__main__":

    path = './cvrp'
    files = par.readInstanceList(path)
    for f in files:
        graphToSolve =  par.createGraph(f)
        sol.ClarkeWright(graphToSolve)
