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
import time


if __name__ == "__main__":

    path = './cvrp'
    files = par.readInstanceList(path)
    for f in files:
      graphToSolve =  par.createGraph(path,f)
      
      start_time_seq =time.time()

      # solutionSequential = sol.ClarkeWright(graphToSolve,False)
      # if(sol.SearchaAndCompleteSequence(solutionSequential,graphToSolve)):
      #     print("Solution Clarke and Wright Sequential Invalid ") 
      # else:
      #     sol.writeResult(solutionSequential,graphToSolve,start_time_seq,"mysol") 

      # start_time_par =time.time()
      # solutionParallel = sol.ClarkeWright(graphToSolve,True)
      # if(sol.SearchaAndCompleteSequence(solutionParallel,graphToSolve)):
      #     print("Solution Clarke and Wright Parallel Invalid ") 
      # else:
      #     sol.writeResult(solutionParallel,graphToSolve,start_time_par,"mysol_par") 

      GAPassignementRR =-1
      GAPassignementRand = -1

      n_vehicles = int( math.ceil(graphToSolve.getTotalDemand() /  graphToSolve.getCapacity() ))  

      while(GAPassignementRR == -1):  
        start_time_clustering = time.time ()   
        K_clusterRR = sol.FisherJaikumar_Kselector(graphToSolve,n_vehicles)           
        GAPassignementRR = sol.GAPsolver(graphToSolve,K_clusterRR)
        start_time_clustering = (time.time() - start_time_clustering)
        if(GAPassignementRR != -1):
            start_time_sol1 =  time.time()
            solution = sol.FisherJaikumar_Routing(graphToSolve,GAPassignementRR,K_clusterRR,"mysol_FJ")
            if(sol.SearchaAndCompleteSequence(solution,graphToSolve)):
              print("Solution Routing NN RR Invalid! ") 
            else:
              sol.writeResult(solution,graphToSolve,(start_time_sol1 - start_time_clustering),"mysol_FJ")
            
            start_time_sol2 = time.time()
            solution2 = sol.FisherJaikumar_Routing_Dijkastra(graphToSolve,GAPassignementRR,K_clusterRR,"mysol_DJ")         
            if(sol.SearchaAndCompleteSequence(solution2,graphToSolve)):
              print("Solution Routing in DIjkastra RR Invalid! ")
            else:
              sol.writeResult(solution2,graphToSolve,(start_time_sol2 - start_time_clustering ),"mysol_DJ")   
        else:
          n_vehicles = n_vehicles +1


      n_vehicles = 0
      while(GAPassignementRand == -1):
        start_time_clustering34 = time.time()   
        K_clusterRand = [random.randint(1,graphToSolve.getDimension()-1) for i in range(n_vehicles)]
        GAPassignementRand = sol.GAPsolver(graphToSolve,K_clusterRand)
        start_time_clustering34 = (time.time() - start_time_clustering34)
        if(GAPassignementRand != -1):
            start_time_sol3 =time.time()
            solution = sol.FisherJaikumar_Routing(graphToSolve,GAPassignementRand,K_clusterRand,"mysol_FJ_kRand")
            if(sol.SearchaAndCompleteSequence(solution,graphToSolve)):
              print("Solution Routing NN Random Invalid! ! ")
            else :
              sol.writeResult(solution,graphToSolve,(start_time_sol3 - start_time_clustering34),"mysol_FJ_kRand")

            start_time_sol4 =time.time()
            solution2 = sol.FisherJaikumar_Routing_Dijkastra(graphToSolve,GAPassignementRand,K_clusterRand,"mysol_DJ_kRand")          
            if(sol.SearchaAndCompleteSequence(solution2,graphToSolve)):
              print("Solution Routing in DIjkastra Random Invalid! ") 
            else:
              sol.writeResult(solution2,graphToSolve,(start_time_sol4 - start_time_clustering34 ),"mysol_DJ_kRand")
        else:
          n_vehicles = n_vehicles +1
        
      # start_time =time.time ()
      # solution3 = sol.ClusterFirst_RouteSecond(graphToSolve,"Sol_CR")
      # if(sol.SearchaAndCompleteSequence(solution3,graphToSolve)):
      #   print("Solution Cluster First Route Second ") 
      # else:
      #   sol.writeResult(solution3,graphToSolve,start_time,"Sol_CR")   


      # start_time = time.time ()
      # #Parameters setting: percentage of Elitism, threshold of improving fitting, number of cromosome
      # mutationRate = 1
      # n_population = 100
      # population = []
      # elitismList =[]
      # Eras = 40
      # era = 0
      # n_vehicles = int( math.ceil(graphToSolve.getTotalDemand() /  graphToSolve.getCapacity() ))           

      # #Initialize Population : Select k customers, create routes and calculate fitness of each chromosome
      # for i in range(n_population):
      #   K_clusterRand = [random.randint(1,graphToSolve.getDimension()-1) for i in range(n_vehicles)]
      #   GAPassignementRand = sol.GAPsolver(graphToSolve,K_clusterRand)
      #   #K_clusterRR = sol.FisherJaikumar_Kselector(graphToSolve,n_vehicles)           
      #   #GAPassignementRR = sol.GAPsolver(graphToSolve,K_clusterRR)
      #   if(GAPassignementRand != -1):
      #     chromosome = sol.FisherJaikumar_Routing(graphToSolve,GAPassignementRand,K_clusterRand,"trash") 
      #     if(sol.SearchaAndCompleteSequence(chromosome,graphToSolve)):
      #       print("Invalid! ")
      #     else:
      #       population.append((sum([c.getCost() for c in chromosome]),chromosome))
      #   #else:
      #     #n_vehicles = n_vehicles + 1
            
      # #Stop Criterion
      # while(era < Eras):
      #   print("Welcome to the ==> " + str(era) +" Era!")
      #   toKeep = sol.Elitism(population)
      #   popEra = []
      #   #tabuLister = []
      #   #Do evolutionary opeeration half time population
      #   for k in range(int(len(population)/2)):      
      #     winner1,winner2 ,f1,f2= sol.Tournament(population,True)   
      #     if (np.random.randint(1,100) <= 1):
      #        f1, winner1 = toKeep
            
      #     children, tabuLister , fittingCrossover = sol.Crossover(winner1,winner2,graphToSolve,True)
      #     if (fittingCrossover>f1 or fittingCrossover>f2):
      #         continue
      #     print("CROSSOVER ==> "+str(fittingCrossover))
              
      #     if(sol.SearchaAndCompleteSequence(children,graphToSolve)):
      #        print("Invalid! " +str(fittingCrossover))
      #        continue
      #     else:
      #       popEra.append((fittingCrossover,children))
          
      #     # if (np.random.randint(1,100) <= mutationRate):
      #     #   popEra.sort(key=lambda x:x[0],reverse=True)
      #     #   if(len(popEra)>0):
      #     #     mutantChild = popEra.pop()
      #     #   else: break 
      #     #   mutant = sol.Mutation(mutantChild[1],graphToSolve,1)
      #     #   fittingMutation = sum([m.getCost() for m in mutant])
      #     #   if(fittingMutation < mutantChild[0]):
      #     #     if(sol.SearchaAndCompleteSequence(mutant,graphToSolve)):
      #     #         print("Invalid! " +str(fittingCrossover))
      #     #         continue
      #     #     else:
      #     #         popEra.append((fittingMutation,mutant))
      #     #         print("CROSSOVER + MUTATION  HARD ==> "+str(fittingMutation))
           
      #     if (np.random.randint(1,100) <= mutationRate):
      #       popEra.sort(key=lambda x:x[0],reverse=True)
      #       if(len(popEra)>0):
      #         mutantChild = popEra[0]
      #       else: break

      #       for route in mutantChild[1]:
      #           c1 = np.random.randint(1,len(route.getCustomers())-1)
      #           c2 = np.random.randint(1,len(route.getCustomers())-1)
      #           route = sol.LocalSearch_FlippingPath(route,graphToSolve,c1,c2)

      #       fittingMutation = sum([m.getCost() for m in mutantChild[1]])
      #       if(fittingMutation < mutantChild[0]):
      #         if(sol.SearchaAndCompleteSequence(mutantChild[1],graphToSolve)):
      #           print("Invalid! " +str(fittingCrossover))
      #           continue
      #         else:
      #           popEra.append((fittingMutation,mutantChild[1]))
      #           print("CROSSOVER + MUTATION FLIPPING  ==> "+str(fittingMutation))

      #   popEra.sort(key=lambda x:x[0],reverse=True)
      #   best = [popEra.pop() for i in range(int(len(popEra)/2))]


      #   for b in best:
      #     for p in population:        
      #       if(b[0] not in [ps[0] for ps in population]):
      #         if(p[0] > b[0]):
      #           population.remove(p)
      #           population.append(b)
      #           break
      #       else: break

      #   if toKeep not in population:
      #     population.append(toKeep)
      #   era = era + 1
          
      # population.sort(key= lambda x: x[0], reverse = True)
      # bestGeneticSolution = population.pop()[1]    
      # sol.writeResult(bestGeneticSolution,graphToSolve,start_time,"mysol_Genetic")
      
  
          

        
    print("==============================CLARKE AND WRIGHT SEQUENTIAL==================================")   
    sol.printResult('./cvrp-sol','./mysol')
    print("==============================CLARKE AND WRIGHT PARALLEL==================================")   
    sol.printResult('./cvrp-sol','./mysol_par')
    print("==============================FISHER AND JAIKUMAR ==================================")       
    sol.printResult('./cvrp-sol','./mysol_FJ')
    print("==============================MODIFIED DIJKASTRA ==================================") 
    sol.printResult('./cvrp-sol','./mysol_DJ')
    print("======================FISHER AND JAIKUMAR ON RANDOM K ==================================") 
    sol.printResult('./cvrp-sol','./mysol_FJ_kRand')
    print("======================MODIFIED DIJKASTRA  ON RANDOM K ==================================") 
    sol.printResult('./cvrp-sol','./mysol_DJ_kRand')
    print("============================== GENETIC ON DIJ-KSEL   ==================================")  
    sol.printResult('./cvrp-sol','./mysol_Genetic')
    print("======================DIJKASTRA CLUSTER FIRST ROUTE SECOND==================================") 
    sol.printResult('./cvrp-sol','./Sol_CR')
  
           
    # print("==============================CLARKE AND WRIGHT==================================")   
    # sol.printResult('./A-VRP//A-opt','./mysol')
    # print("============A-VRP/==================FISHER AND JAIKUMAR ==================================")       
    # sol.printResult('./A-VRP/A-opt','./mysol_FJ')
    # print("============A-VRP/==================MODIFIED DIJKASTRA ==================================") 
    # sol.printResult('./A-VRP/A-opt','./mysol_DJ')
    # print("============A-VRP/==========FISHER AND JAIKUMAR ON RANDOM K ==================================") 
    # sol.printResult('./A-VRP/A-opt','./mysol_FJ_kRand')
    # print("============A-VRP/================== GENETIC ON FJ SOL WITH RANDOM k  ==================================")  
    # sol.printResult('./A-VRP/A-opt','./mysol_Genetic')
    # print("============A-VRP/==========DIJKASTRA RANDOM K ==================================") 
    # sol.printResult('./A-VRP/A-opt','./mysol_DJ_kRand')
    # print("============A-VRP/==========DIJKASTRA CLUSTER FIRST ROUTE SECOND==================================") 
    # sol.printResult('./A-VRP/A-opt','./Sol_CR')





                  


    

        



