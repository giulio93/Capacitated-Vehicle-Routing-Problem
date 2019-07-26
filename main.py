# coding: utf-8

import os
import parser as par
import solver as sol

if __name__ == "__main__":

    path = './cvrp'
    #graphToSolve =  par.createGraph('bayg-n29-k4.vrp')
    files = par.readInstanceList(path)
    for f in files:
        graphToSolve =  par.createGraph(f)
        sol.FisherJaikumar(graphToSolve,5)

    #     sol.ClarkeWright(graphToSolve)

    # path='./mysol'
    # mysol = par.readInstanceList(path)
    # path2='./cvrp-sol'
    # cvrp_sol = par.readInstanceList(path2)
    # for sol in mysol:
    #     with open(path+'/'+sol, "r+") as f:
    #         for line in f:
    #             keywords = line
    #             if(keywords.split(':')[0].strip()=="Routing Total Cost"):
    #                 stimated = float(keywords.split(':')[1].strip())
    #                 for optimal in cvrp_sol:
    #                     with open(path2+'/'+optimal, "r") as c:
    #                         if(sol.split('.')[0] == "Sol_"+optimal.split('.')[0]):
    #                             for linec in c:
    #                                 keys = linec                                   
    #                                 if(len(keys.split()) > 0 and keys.split()[0].strip()=="Cost"):
    #                                     actual = float(keys.split()[1].strip())
    #                                     error = (stimated - actual)/actual
    #                                     print("Error of solution in "+sol + ": "+ str(float(error)))
    #                                     f.write("Error of solution in "+sol + ": "+ str(float(error)))


                  


    

        
