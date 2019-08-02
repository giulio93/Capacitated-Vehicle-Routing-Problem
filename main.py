# coding: utf-8


import os
import sys
sys.path.append(os.getcwd()+'/Giulio/Capacitated-Vehicle-Routing-Problem')
import parser as par
import solver as sol
import math 
import random
from route import Route


if __name__ == "__main__":

    path = './cvrp'
    #graphToSolve =  par.createGraph('bayg-n29-k4.vrp')
    files = par.readInstanceList(path)
    for f in files:
      graphToSolve =  par.createGraph(f)
      #  sol.ClarkeWright(graphToSolve)
      n_vehicles = int( math.ceil(graphToSolve.getTotalDemand() /  graphToSolve.getCapacity() ))
      #  K_cluster = sol.FisherJaikumar_Kselector(graphToSolve,7)
      #  K_clusterRR = sol.FisherJaikumar_Kselector(graphToSolve,n_vehicles)
      K_clusterRand = [random.randint(1,graphToSolve.getDimension()-1) for i in range(n_vehicles)]
      #  GAPassignementRR = sol.GAPsolver(graphToSolve,K_clusterRR)
      #  GAPassignementRand = sol.GAPsolver(graphToSolve,K_clusterRand)
      #  sol.FisherJaikumar_Routing(graphToSolve,GAPassignementRR,K_clusterRR,"mysol_FJ")
      #  sol.FisherJaikumar_Routing_Dijkastra(graphToSolve,GAPassignementRR,K_clusterRR,"mysol_DJ")       
      #  sol.FisherJaikumar_Routing(graphToSolve,GAPassignementRand,K_clusterRand,"mysol_FJ_kRand")
      #  sol.FisherJaikumar_Routing_Dijkastra(graphToSolve,GAPassignementRand,K_clusterRand,"mysol_DJ_kRand")
      #sol.ClusterFirst_RouteSecond(graphToSolve,"Sol_CR")

      n_evolution = 10
      while n_evolution > 0 :
        #Population Generation
        percentage = 1
        K_clusterRand = [random.randint(1,graphToSolve.getDimension()-1) for i in range(n_vehicles)]
        GAPassignementRR = sol.GAPsolver(graphToSolve,K_clusterRand)
        population = sol.FisherJaikumar_Routing(graphToSolve,GAPassignementRR,K_clusterRand,"mysol_FJ")
        fitness, copied = sol.Elitism(population,percentage)
        winnerCandidates = sol.Tournament(fitness,copied)
        sol.Crossover(winnerCandidates,graphToSolve)

        

        


              



        

    
   
    print("==============================CLARKE AND WRIGHT==================================")   
    sol.printResult('./cvrp-sol','./mysol')
    print("==============================FISHER AND JAIKUMAR ==================================")       
    sol.printResult('./cvrp-sol','./mysol_FJ')
    print("==============================MODIFIED DIJKASTRA ==================================") 
    sol.printResult('./cvrp-sol','./mysol_DJ')
    print("======================FISHER AND JAIKUMAR ON RANDOM K==================================") 
    sol.printResult('./cvrp-sol','./mysol_FJ_kRand')
    print("======================DIJKASTRA RANDOM K==================================") 
    sol.printResult('./cvrp-sol','./mysol_DJ_kRand')
    print("======================DIJKASTRA CLUSTER FIRST ROUTE SECOND==================================") 
    sol.printResult('./cvrp-sol','./Sol_CR')




                  


    

        



