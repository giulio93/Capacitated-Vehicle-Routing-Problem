# coding: utf-8


import os
import sys
sys.path.append(os.getcwd()+'/Giulio/Capacitated-Vehicle-Routing-Problem')
import parser as par
import solver as sol
import math 
import random
from route import Route
import numpy as np


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
      #K_clusterRand = [random.randint(1,graphToSolve.getDimension()-1) for i in range(n_vehicles)]
      #  GAPassignementRR = sol.GAPsolver(graphToSolve,K_clusterRR)
      #  GAPassignementRand = sol.GAPsolver(graphToSolve,K_clusterRand)
      #  sol.FisherJaikumar_Routing(graphToSolve,GAPassignementRR,K_clusterRR,"mysol_FJ")
      #  sol.FisherJaikumar_Routing_Dijkastra(graphToSolve,GAPassignementRR,K_clusterRR,"mysol_DJ")       
      #  sol.FisherJaikumar_Routing(graphToSolve,GAPassignementRand,K_clusterRand,"mysol_FJ_kRand")
      #  sol.FisherJaikumar_Routing_Dijkastra(graphToSolve,GAPassignementRand,K_clusterRand,"mysol_DJ_kRand")
      #sol.ClusterFirst_RouteSecond(graphToSolve,"Sol_CR")

     

      #Parameters setting: percentage of Elitism, threshold of improving fitting, number of cromosome
      mutationRate = 1
      n_population = 50
      population = []
      elitismList =[]
      Eras = 20
      era = 0
          #Initialize Population : Select k customers, create routes and calculate fitness of each chromosome
      for i in range(n_population):            
        K_clusterRand = [random.randint(1,graphToSolve.getDimension()-1) for i in range(n_vehicles+1)]
        GAPassignementRR = sol.GAPsolver(graphToSolve,K_clusterRand)
        if(GAPassignementRR != -1):
          chromosome = sol.FisherJaikumar_Routing(graphToSolve,GAPassignementRR,K_clusterRand,"mysol_FJ") 
          if(sol.SearchaAndCompleteSequence(chromosome,graphToSolve)):
            print("Invalid! ")              
          population.append((sum([c.getCost() for c in chromosome]),chromosome))

      #Stop Criterion
      while(era < Eras):
        print("Welcome to the ==> " + str(era) +" Era!")
        toKeep = sol.Elitism(population)
        popEra = []
        #tabuLister = []
        #Do evolutionary opeeration half time population
        for k in range(int(len(population)/2)):
      
          winner1,winner2 ,f1,f2= sol.Tournament(population,True)   
          if (np.random.randint(1,100) <= 1):
             f1, winner1 = toKeep
          children, tabuLister , fittingCrossover = sol.Crossover(winner1,winner2,graphToSolve,True)
          print("CROSSOVER ==> "+str(fittingCrossover))
      
          popEra.append((fittingCrossover,children))
          if(sol.SearchaAndCompleteSequence(children,graphToSolve)):
             print("Invalid! " +str(fittingCrossover))
          else:
            popEra.sort(key=lambda x:x[0],reverse=True)
            mutantChild = popEra[0]
          if (np.random.randint(2,100) <= mutationRate):
            for route in mutantChild[1]:
                c1 = np.random.randint(1,len(route.getCustomers())-1)
                c2 = np.random.randint(1,len(route.getCustomers())-1)
                route = sol.LocalSearch_FlippingPath(route,graphToSolve,c1,c2)

            fittingMutation = sum([m.getCost() for m in children])
            popEra.append((fittingMutation,mutantChild))
            if(sol.SearchaAndCompleteSequence(children,graphToSolve)):
              print("Invalid! " +str(fittingCrossover))
            print("CROSSOVER ==> "+str(fittingMutation))

        popEra.sort(key=lambda x:x[0],reverse=True)
        best = [popEra.pop() for i in range(int(len(popEra)/2))]


        for b in best:
          for p in population:        
            if(b[0] not in [ps[0] for ps in population]):
              if(p[0] > b[0]):
                population.remove(p)
                population.append(b)
                break
            else: break

        if toKeep not in population:
          population.append(toKeep)
        era = era + 1

        
    
      population.sort(key= lambda x: x[0], reverse = True)
      bestGeneticSolution = population.pop()[1]    
      sol.writeResult(bestGeneticSolution,graphToSolve,"mysol_Genetic")
      
  

    
      


          

          

   
    print("==============================CLARKE AND WRIGHT==================================")   
    sol.printResult('./cvrp-sol','./mysol')
    print("==============================FISHER AND JAIKUMAR ==================================")       
    sol.printResult('./cvrp-sol','./mysol_FJ')
    print("==============================MODIFIED DIJKASTRA ==================================") 
    sol.printResult('./cvrp-sol','./mysol_DJ')
    print("======================FISHER AND JAIKUMAR ON RANDOM K==================================") 
    sol.printResult('./cvrp-sol','./mysol_FJ_kRand')
    print("============================== GENETIC ON FJ SOL WITH RANDOM k  ==================================")  
    sol.printResult('./cvrp-sol','./mysol_Genetic')
    print("======================DIJKASTRA RANDOM K==================================") 
    sol.printResult('./cvrp-sol','./mysol_DJ_kRand')
    print("======================DIJKASTRA CLUSTER FIRST ROUTE SECOND==================================") 
    sol.printResult('./cvrp-sol','./Sol_CR')




                  


    

        



