# -*- coding: utf-8 -*-

from domain.map import Map
from domain.population import Population


class Repository:
    def __init__(self):
         
        self.__populations = []
        self.cmap = Map()
        
    def createPopulation(self, args):
        # args = [populationSize, individualSize] -- you can add more args    
        return Population(args[0], args[1])
        
    # TO DO : add the other components for the repository: 
    #    load and save from file, etc
            