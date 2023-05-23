#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 22:09:00 2020

@author: ahmed
"""
import numpy as np
from random import random
from random import randint
from random import shuffle
import seaborn as sns
import matplotlib.pyplot as plt
class strategy():
    def __init__(self,coup1,coup2,mat):
        self.coup1=coup1
        self.coup2=coup2
        self.prob_mat=mat
        self.nom=str(int(mat[0][0]))+"_"+str(int(mat[0][1]))+"_"+str(int(mat[1][0]))+"_"+str(int(mat[1][1]))
        if self.nom=="1_1_1_1":
            self.nom="AG"
        if self.nom=="0_0_0_0":
            self.nom="COOP"
        if self.nom=="0_1_0_1":
            self.nom="TFT"
        if self.nom=="0_0_0_1":
            self.nom="TFTT"
        if self.nom=="0_1_1_1":
            self.nom="TTFT"
    def __eq__(self,strategy):
        return(self.prob_mat==strategy.prob_mat)

    
            
        
#Only 0 et 1  . There are 2*2*2*2 possibilities : 16 
Agression = strategy(0,1,np.ones((2,2)))
Cooperation = strategy(0,0,np.zeros((2,2)))
Alea = strategy(0,0,0.5*np.ones((2,2)))
Tit_For_Tat = strategy(0,0,np.array([[0,1],[0,1]]))
Tit_For_Two_Tats= strategy(0,0,np.array([[0,0],[0,1]]))
Two_Tits_For_Tat = strategy(0,0,np.array([[0,1],[1,1]]))



#ligne 1 prisoner1 cooperates
class prisoner():
    def __init__(self,strategy,n=0):
        self.strategy=strategy
        self.history = [-1,-1]  #zero codes for cooperation, 1 agression,-1 means no history
        self.generation = n
        self.years_due=0 #score
        
    def coup(self,oponent):
        history=oponent.history
        if history[0]>=0:
             history_tup=tuple(history)
             p_agress=self.strategy.prob_mat[history_tup]
             tirage= random()
             if tirage<p_agress:
                 return 1
             else:
                 return 0 
        else : 
            if history[1]>=0:
                return(self.strategy.coup2)
            else:
                return(self.strategy.coup1)
    def continuous_reproduction(self,p2):
        mat_enfant=(self.strategy.prob_mat+p2.strategy.prob_mat)/2
        strat=strategy(self.strategy.coup1,p2.strategy.coup2,mat_enfant)
        p_enfant=prisoner(strat,self.generation+1)
        return(p_enfant)
    def asexual_reproduction(self):
        p_enfant=prisoner(self.strategy,self.generation+1)
        return(p_enfant)
    def reproduction(self,p2):
        tirage1,tirage2=randint(0,1),randint(0,1)
        tirage3,tirage4=randint(0,1),randint(0,1)
        while (tirage3,tirage4)==(tirage1,tirage2):
            tirage3,tirage4=randint(0,1),randint(0,1)
        mat_enfant=self.strategy.prob_mat
        mat_enfant[tirage1,tirage2]=p2.strategy.prob_mat[tirage1,tirage2]
        mat_enfant[tirage3,tirage4]=p2.strategy.prob_mat[tirage3,tirage4]
        strat=strategy(self.strategy.coup1,p2.strategy.coup2,mat_enfant)
        p_enfant=prisoner(strat,self.generation+1)
        return(p_enfant)
    def mutation(self):
        tirage1,tirage2=randint(0,1),randint(0,1)
        strat=self.strategy
        mat=strat.prob_mat.copy()
        mat[tirage1,tirage2]=1-self.strategy.prob_mat[tirage1,tirage2]
        new_strat=strategy(strat.coup1,strat.coup2,mat)
        self.strategy=new_strat
        
    def update(self,coup,years):
        self.history[0]=self.history[1]
        self.history[1]=coup
        self.years_due+=years
    def reset(self):
        self.years_due=0
        self.history = [-1,-1]
class confrontation():
    def __init__(self,prisoner1,prisoner2,round_max):
        self.p1=prisoner1
        self.p2=prisoner2
        self.round_current=0
        self.max=round_max
    def Round(self):
        self.round_current+=1
        #1st prisoner's choice
        coup1 = self.p1.coup(self.p2)
        #2nd prisoner's choice
        coup2 = self.p2.coup(self.p1)
        ag=0
        if coup1==0 and coup2==0:
            years1=1
            years2=1
        if coup1==1 and coup2==1:
            years1=3
            years2=3
            ag=2
        if coup1==0 and coup2==1:
            years1=5
            years2=0
            ag=1
        if coup1==1 and coup2==0:
            years1=0
            years2=5
            ag=1
        self.p1.update(coup1,years1)
        self.p2.update(coup2,years2)
        return(ag)
    def duel(self):
        ag=0
        while self.round_current<self.max:
            ag+=self.Round()
        #Brainwash
        self.p1.history=[-1,-1]
        self.p2.history=[-1,-1]
        return(ag)
        
            
#Tournament: every day, we draw couples
      
class population():
    def __init__(self,liste,max_iterations): 
        self.list_of_prisoners = liste
        self.n = len(liste) #number of prisoners considered (population size)
        self.jour_actuel = 0
        self.max_jours = 100
        self.max_rounds=20 #length of the day
        self.generation_actuelle=0
        self.max_iterations=max_iterations
        self.agressivity=0 #account of the number of times a prisoner betrayed his accomplice.
    def update_pop(self):
        lists=self.list_of_prisoners.copy()
        shuffle(lists)
        for j in range(self.n//2):
            c=confrontation(lists[2*j],lists[2*j+1],self.max_rounds)
            self.agressivity+=c.duel()
        self.jour_actuel+=1
    def let_evolution_asexual_work(self):
        liste_agressivity=[]
        liste_bienveillance=[]
        while self.generation_actuelle<self.max_iterations:
            while self.jour_actuel<self.max_jours:
                self.update_pop()
            liste_bienveillance.append(self.stats_population())
            self.list_of_prisoners=sorted(self.list_of_prisoners, key=lambda k: k.years_due)[0:self.n//2]
            for i in range(self.n//2):
                pris=self.list_of_prisoners[i]
                pp=pris.asexual_reproduction()
                
                #MUTATION
                tirage= random()
                if tirage<0.05:
                    pp.mutation()
                self.list_of_prisoners.append(pp)
                pris.reset()
            self.generation_actuelle+=1
            self.jour_actuel=0
            liste_agressivity.append(self.agressivity)
            self.agressivity=0
        plt.style.use('seaborn')
        plt.plot(liste_agressivity)
        plt.show()
        plt.plot(liste_bienveillance)
        plt.show()
        
    def let_evolution_continuous_work(self):
        liste_agressivity=[]
        while self.generation_actuelle<self.max_iterations:
            while self.jour_actuel<self.max_jours:
                self.update_pop()
            self.list_of_prisoners=sorted(self.list_of_prisoners, key=lambda k: k.years_due)[0:2*self.n//3]
            shuffle(self.list_of_prisoners)
            for i in range(self.n//3):
                pris=self.list_of_prisoners[i]
                pris2=self.list_of_prisoners[2*i]
                pp=pris.continuous_reproduction(pris2)
                
                #MUTATION
                tirage= random()
                if tirage<0.05:
                    pp.mutation()
                self.list_of_prisoners.append(pp)
                pris.reset()
            self.generation_actuelle+=1
            self.jour_actuel=0
            liste_agressivity.append(self.agressivity)
            self.agressivity=0
        plt.style.use('seaborn')
        plt.plot(liste_agressivity)
        plt.show()       
    def let_evolution_work(self):
        liste_agressivity=[]
        liste_bienveillance=[]
        while self.generation_actuelle<self.max_iterations:
            while self.jour_actuel<self.max_jours:
                self.update_pop()
            liste_bienveillance.append(self.stats_population())
            self.list_of_prisoners=sorted(self.list_of_prisoners, key=lambda k: k.years_due)[0:2*self.n//3]
            shuffle(self.list_of_prisoners)
            for i in range(self.n//3):
                pris=self.list_of_prisoners[i]
                pris2=self.list_of_prisoners[2*i]
                pp=pris.reproduction(pris2)
                
                #MUTATION
                tirage= random()
                if tirage<0.05:
                    pp.mutation()
                self.list_of_prisoners.append(pp)
                pris.reset()
            self.generation_actuelle+=1
            self.jour_actuel=0
            liste_agressivity.append(self.agressivity)
            self.agressivity=0
        plt.style.use('seaborn')
        plt.plot(liste_agressivity)
        plt.show()
        plt.plot(liste_bienveillance)
        plt.show()
            
            
    def stats_population(self):#statistiques sur la generation actuelle.
      
        x=[]
        y=[]
        for j in range(self.n):
#            y.append(self.list_of_prisoners[j].years_due)
#            x.append(self.list_of_prisoners[j].strategy.nom) 
            if self.list_of_prisoners[j].strategy.prob_mat[0,0]==0:#counts those who aren't unusefully agressive
                nb_forgiving+=1
            
           
#        plt.style.use('seaborn')       
#        plt.scatter(x,y)
#        plt.show()
        return(nb_forgiving)
        
    def stats_pop(self): # Plots the proportion of each strategy in the population
        x=[]
        y=[]
        z=[]
        for j in range(self.n):
           x.append(self.list_of_prisoners[j].strategy.nom) 
        from collections import Counter
        c = Counter(x)   
        for i in c:
            y.append(c[i])
            z.append(str(i))
        plt.scatter(z,y)
           
        

def axelrod_tournament(number_of_clones,number_generations): # Iterated Axelrod tournament
    population1 = []
    Strategies= [Agression,Agression,Cooperation,Tit_For_Tat,Tit_For_Two_Tats,Two_Tits_For_Tat]
    for i in range(number_of_clones):
        for j in range(len(Strategies)):
            p=prisoner(Strategies[j])
            population1.append(p)
    pop=population(population1,number_generations)
    pop.let_evolution_work()
    pop.stats_pop()
    return(pop)
    
    