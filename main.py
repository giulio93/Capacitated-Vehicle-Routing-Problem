# coding: utf-8

import os
import parser as par

if __name__ == "__main__":

    path = './cvrp'
    files = par.readInstanceList(path)
    par.createGraph(files)