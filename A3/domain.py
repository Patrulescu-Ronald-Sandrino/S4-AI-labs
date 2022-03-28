# -*- coding: utf-8 -*-
from random import *


# the glass gene can be replaced with int or float, or other types
# depending on your problem's representation


class gene:
    def __init__(self):
        # random initialise the gene according to the representation
        pass


class Individual:
    def __init__(self, size = 0):
        self.__size = size
        self.__x = [gene() for i in range(self.__size)]
        self.__f = None
        
    def fitness(self):
        # compute the fitness for the indivisual
        # and save it in self.__f
        pass
    
    def mutate(self, mutateProbability = 0.04):
        if random() < mutateProbability:
            pass
            # perform a mutation with respect to the representation
        
    
    def crossover(self, otherParent, crossoverProbability = 0.8):
        offspring1, offspring2 = Individual(self.__size), Individual(self.__size) 
        if random() < crossoverProbability:
            pass
            # perform the crossover between the self and the otherParent 
        
        return offspring1, offspring2


class Population:
    def __init__(self, populationSize = 0, individualSize = 0):
        self.__populationSize = populationSize
        self.__v = [Individual(individualSize) for x in range(populationSize)]
        
    def evaluate(self):
        # evaluates the population
        for x in self.__v:
            x.fitness()
            
    def selection(self, k=0):
        # perform a selection of k individuals from the population
        # and returns that selection
        pass


