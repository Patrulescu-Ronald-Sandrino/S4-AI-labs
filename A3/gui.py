# -*- coding: utf-8 -*-
from typing import Tuple

import pygame
import time
from pygame.locals import *

from controller import Controller
from utils import *


class GUI:
    def __init__(self,
                 controller: Controller,
                 dimension: Tuple[int, int] = DEFAULT_SCREEN_DIMENSION,
                 window_title: str = "drone exploration with AE",
                 logo_image_path: str = "assets/logo32x32.png",
                 screen_fill: Tuple[int, int, int] = Color.WHITE):
        self.__controller = controller
        pygame.init()
        pygame.display.set_caption(window_title)
        pygame.display.set_icon(pygame.image.load(logo_image_path))
        self.__screen = pygame.display.set_mode(dimension)  # opens the window
        self.__screen.fill(screen_fill)

    @staticmethod
    def close_pygame():
        # closes the pygame
        running = True
        # loop for events
        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False
        pygame.quit()


def init_pygame(dimension):
    # init the pygame
    pygame.init()
    logo = pygame.image.load("assets/logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("drone exploration with AE")
    
    # create a surface on screen that has the size of 800 x 480
    screen = pygame.display.set_mode(dimension)  # opens the window
    screen.fill(Color.WHITE)
    return screen


def close_pygame():
    # closes the pygame
    running = True
    # loop for events
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
    pygame.quit()
    

def moving_drone(current_map, path, speed: int = 1, mark_seen = True):
    # animation of a drone on a path
    
    screen = init_pygame((current_map.__rows * 20, current_map.__columns * 20))

    drona = pygame.image.load("assets/drona.png")
        
    for i in range(len(path)):
        screen.blit(image(current_map), (0, 0))
        
        if mark_seen:
            brick = pygame.Surface((20, 20))
            brick.fill(Color.GREEN)
            for j in range(i+1):
                for (delta_x, delta_y) in DIRECTIONS:
                    x = path[j][0]
                    y = path[j][1]
                    while ((0 <= x + delta_x < current_map.__rows and
                            0 <= y + delta_y < current_map.__columns) and
                           current_map.__surface[x + delta_x][y + delta_y] != 1):
                        x = x + delta_x
                        y = y + delta_y
                        screen.blit(brick, (y * 20, x * 20))
        
        screen.blit(drona, (path[i][1] * 20, path[i][0] * 20))
        pygame.display.flip()
        time.sleep(0.5 * speed)            
    close_pygame()


def moving_drone2(current_map, path_as_directions, speed: int = 1, mark_seen = True):
    # animation of a drone on a path

    screen = init_pygame((current_map.__rows * 20, current_map.__columns * 20))

    drona = pygame.image.load("assets/drona.png")

    for i in range(len(path_as_directions)):
        screen.blit(image(current_map), (0, 0))

        if mark_seen:
            brick = pygame.Surface((20, 20))
            brick.fill(Color.GREEN)
            for j in range(i+1):
                for (delta_x, delta_y) in DIRECTIONS:
                    x = path_as_directions[j][0]
                    y = path_as_directions[j][1]
                    while ((0 <= x + delta_x < current_map.__rows and
                            0 <= y + delta_y < current_map.__columns) and
                           current_map.__surface[x + delta_x][y + delta_y] != 1):
                        x = x + delta_x
                        y = y + delta_y
                        screen.blit(brick, (y * 20, x * 20))

        screen.blit(drona, (path_as_directions[i][1] * 20, path_as_directions[i][0] * 20))
        pygame.display.flip()
        time.sleep(0.5 * speed)
    close_pygame()


def image(current_map, colour: Tuple[int, int, int] = Color.BLUE, background: Tuple[int, int, int] = Color.WHITE):
    # creates the image of a map
    
    imagine = pygame.Surface((current_map.__rows * 20, current_map.__columns * 20))
    brick = pygame.Surface((20, 20))
    brick.fill(colour)
    imagine.fill(background)
    for i in range(current_map.__rows):
        for j in range(current_map.__columns):
            if current_map.__surface[i][j] == 1:
                imagine.blit(brick, (j * 20, i * 20))
                
    return imagine        
    