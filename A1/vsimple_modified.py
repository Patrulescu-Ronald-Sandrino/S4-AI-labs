#!/usr/bin/python

# import the pygame module, so you can use it
import pickle,pygame,sys
from pygame.locals import *
from random import random, randint
import numpy as np

import time as tm
import os


#Creating some colors
BLUE  = (0, 0, 255)
GRAYBLUE = (50,120,120)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

#define indexes variations 
v = [[-1, 0], [1, 0], [0, 1], [0, -1]]


class Environment():
    def __init__(self):
        self.__n = 20
        self.__m = 20
        self.__surface = np.zeros((self.__n, self.__m))
    
    def randomMap(self, fill = 0.2):
        for i in range(self.__n):
            for j in range(self.__m):
                if random() <= fill :
                    self.__surface[i][j] = 1
                
    def __str__(self):
        string=""
        for i in range(self.__n):
            for j in range(self.__m):
                string = string + str(int(self.__surface[i][j]))
            string = string + "\n"
        return string[:-1]

    def str2(self):
        string = ""
        for i in range(self.__n):
            for j in range(self.__m):
                string = string + "e[" + str(i) + "][" + str(j) + "] = " + str(int(self.__surface[i][j])) + "\n"
            string = string + "\n"
        return string
                
    def readUDMSensors(self, x,y):
        readings=[0,0,0,0]
        # UP 
        xf = x - 1
        while ((xf >= 0) and (self.__surface[xf][y] == 0)):
            xf = xf - 1
            readings[UP] = readings[UP] + 1
        # DOWN
        xf = x + 1
        while ((xf < self.__n) and (self.__surface[xf][y] == 0)):
            xf = xf + 1
            readings[DOWN] = readings[DOWN] + 1
        # LEFT
        yf = y + 1
        while ((yf < self.__m) and (self.__surface[x][yf] == 0)):
            yf = yf + 1
            readings[LEFT] = readings[LEFT] + 1
        # RIGHT
        yf = y - 1
        while ((yf >= 0) and (self.__surface[x][yf] == 0)):
            yf = yf - 1
            readings[RIGHT] = readings[RIGHT] + 1
     
        return readings
    
    def saveEnvironment(self, numFile):
        with open(numFile,'wb') as f:
            pickle.dump(self, f)
            f.close()
        
    def loadEnvironment(self, numfile):
        with open(numfile, "rb") as f:
            dummy = pickle.load(f)
            self.__n = dummy.__n
            self.__m = dummy.__m
            self.__surface = dummy.__surface
            f.close()
        
    def image(self, colour = BLUE, background = WHITE):
        imagine = pygame.Surface((420,420))
        brick = pygame.Surface((20,20))
        brick.fill(BLUE)
        imagine.fill(WHITE)
        for i in range(self.__n):
            for j in range(self.__m):
                if (self.__surface[i][j] == 1):
                    imagine.blit(brick, ( j * 20, i * 20))
                
        return imagine        
        
        
class DMap():
    def __init__(self):
        self.__n = 20
        self.__m = 20
        self.surface = np.zeros((self.__n, self.__m))
        for i in range(self.__n):
            for j in range(self.__m):
                self.surface[i][j] = valueOfUnexploredCell
        
        
    def markDetectedWalls(self, e, x, y):
        #   To DO
        # mark on this map the wals that you detect
        wals = e.readUDMSensors(x, y)
        i = x - 1
        if wals[UP] > 0:
            while ((i>=0) and (i >= x - wals[UP])):
                self.surface[i][y] = 0
                i = i - 1
        if (i>=0):
            self.surface[i][y] = 1
            
        i = x + 1
        if wals[DOWN] > 0:
            while ((i < self.__n) and (i <= x + wals[DOWN])):
                self.surface[i][y] = 0
                i = i + 1
        if (i < self.__n):
            self.surface[i][y] = 1
            
        j = y + 1
        if wals[LEFT] > 0:
            while ((j < self.__m) and (j <= y + wals[LEFT])):
                self.surface[x][j] = 0
                j = j + 1
        if (j < self.__m):
            self.surface[x][j] = 1
        
        j = y - 1
        if wals[RIGHT] > 0:
            while ((j >= 0) and (j >= y - wals[RIGHT])):
                self.surface[x][j] = 0
                j = j - 1
        if (j >= 0):
            self.surface[x][j] = 1
        
        return None
        
    def image(self, x, y):
        
        imagine = pygame.Surface((420,420))
        brick = pygame.Surface((20,20))
        empty = pygame.Surface((20,20))
        empty.fill(WHITE)
        brick.fill(BLACK)
        imagine.fill(GRAYBLUE)
        
        for i in range(self.__n):
            for j in range(self.__m):
                if (self.surface[i][j] == 1):
                    imagine.blit(brick, ( j * 20, i * 20))
                elif (self.surface[i][j] == 0):
                    imagine.blit(empty, ( j * 20, i * 20))
                
        drona = pygame.image.load("drona.png")
        imagine.blit(drona, (y *20, x*20))
        return imagine

    def __str__(self):
        string=""
        for i in range(self.__n):
            for j in range(self.__m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string[:-1]
        
        
class Drone():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def move(self, detectedMap):
        pressed_keys = pygame.key.get_pressed()
        if self.x > 0:
            if pressed_keys[K_UP] and detectedMap.surface[self.x-1][self.y]==0:
                self.x = self.x - 1
        if self.x < 19:
            if pressed_keys[K_DOWN] and detectedMap.surface[self.x+1][self.y]==0:
                self.x = self.x + 1
        
        if self.y > 0:
              if pressed_keys[K_LEFT]and detectedMap.surface[self.x][self.y-1]==0:
                  self.y = self.y - 1
        if self.y < 19:        
              if pressed_keys[K_RIGHT] and detectedMap.surface[self.x][self.y+1]==0:
                  self.y = self.y + 1
                  
    def moveDSF(self, detectedMap):
         # TO DO!
         #rewrite this function in such a way that you perform an automatic 
         # mapping with DFS           
        # start

        is1DPositionValid = lambda value: 0 <= value <= 19
        is2DPositionValid = lambda x, y: is1DPositionValid(x) and is1DPositionValid(y)
        def isChildValid(x, y):
            return is2DPositionValid(x, y)
        is2DPositionOnEdge = lambda x, y: x in [0, 19] or y in [0, 19]
        shouldSkip2DPosition = lambda x, y: is2DPositionOnEdge(x, y) and detectedMap.surface[x][y] == 0

        def getValidNext2DPositions(x, y):
            result = []

            for (delta_x, delta_y) in v:
                next2DPosition = (x + delta_x, y + delta_y)

                if is2DPositionValid(*next2DPosition):
                    result.append(next2DPosition)

            return result



        """
        depth >= 0

        call with: distanceToClosestUnexplored((x, y) + dir, depth, dir)
        """
        def distanceToClosestUnexplored(x, y, depth, direction_from_source=None):
            if depth < 0:
                return -1
            if detectedMap.surface[x][y] == valueOfUnexploredCell:
                return 0

            minimumDistance = float('+inf')
            for direction in DIRECTIONS:
                if direction = INVERSE[direction_from_source]:
                    continue
                [dx, dy] = direction
                next2DPosition = (x + dx, y + dy)
                if not is2DPositionValid(*next2DPosition):
                    continue

                minimumDistance = min(minimumDistance, 1 + distanceToClosestUnexplored(x + dx, y + dy, depth - 1, direction))
            return minimumDistance


        found = False
        visited = {}
        toVisit = [(self.x, self.y)]
        detectedMap.surface[self.x][self.y] = 0 # <-- very bad without (x, y) != (self.x, self.y) condition

        while not found and len(toVisit) > 0:
            (x, y) = toVisit.pop(0)
            visited[(x, y)] = 1

            if debug:
                print("(self.x, self.y) = ", (self.x, self.y))
                print("(x,y) = ", (x, y))
                print("toVisit = ", toVisit)
                print(str(detectedMap))

            if detectedMap.surface[x][y] == 0 and (x, y) != (self.x, self.y): # to avoid going back were we started
                self.x, self.y = x, y
                if debug:
                    print("found ", (x, y), '\n')
                found = True # or just: return
            else:
                unvisitedChildren = []

                for direction in DIRECTIONS:
                    [dx, dy] = direction
                    child =  (x + dx, y + dy)
                    
                    if child in visited:
                        continue
                    if not isChildValid(*child): # only valid positions inside the map should be added
                        continue
                    # if shouldSkip2DPosition(*child):
                    #    continue

                    if CHILD_GENERATOR_VERSION == 1:
                        unvisitedChildren.append(child)
                    elif CHILD_GENERATOR_VERSION == 2:
                        currentDistance = distanceToClosestUnexplored(*child, DEPTH, direction)
                        # TODO: add to unvisitedChildren, ordered by distanceToClosestUnexplored
                    else:
                        print('Drone.moveDFS() Error: CHILD_GENERATOR_VERSION not reconized')
                        os._exit(1)

                toVisit = unvisitedChildren + toVisit
        
debug = True
valueOfUnexploredCell = 7 # TODO: change back to -1 when done with debug printing
moved = 0
sleepTime = 1
DIRECTIONS = [[-1, 0], [0, 1], [1, 0], [0, -1]] # LEFT UP RIGHT DOWN
INVERSE = {}
INVERSE[[-1, 0]] = [1, 0]
INVERSE[[1, 0]] = [-1, 0]
INVERSE[[0, 1]] = [0, -1]
INVERSE[[0, -1]] = [0, 1]
DEPTH = 20
CHILD_GENERATOR_VERSION = 2

                  
# define a main function
def main():
    #we create the environment
    e = Environment()
    e.loadEnvironment("test2.map")
    #print(str(e))
    
    # we create the map
    m = DMap() 
    
    
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("drone exploration")
        
    
    
    # we position the drone somewhere in the area
    x = randint(0, 19)
    y = randint(0, 19)
    
    #cream drona
    d = Drone(x, y)
    
    
    if debug:
        print("Drone starts at ", (x, y))
        print("Map is")
        print(str(e))
    # create a surface on screen that has the size of 800 x 480
    screen = pygame.display.set_mode((800,400))
    screen.fill(WHITE)
    screen.blit(e.image(), (0,0))
    
    # define a variable to control the main loop
    running = True
     
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            #if event.type == KEYDOWN:
                # use this function instead of move
                #d.move(m)
            else:
                """
                d.moveDSF(m)
                print("moved")
                tm.sleep(10)
                """

        m.markDetectedWalls(e, d.x, d.y)
        screen.blit(m.image(d.x,d.y),(400,0))
        pygame.display.flip()

        d.moveDSF(m)
        global moved
        moved += 1
        if debug:
            print("moved", moved, "times")
        tm.sleep(sleepTime)

       
    pygame.quit()
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
