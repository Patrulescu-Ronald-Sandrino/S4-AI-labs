import pygame
from pygame.constants import K_UP, K_DOWN, K_LEFT, K_RIGHT


class Drone:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_position(self, x, y):
        self.x, self.y = x, y

    def move(self, detected_map):
        pressed_keys = pygame.key.get_pressed()
        if self.x > 0:
            if pressed_keys[K_UP] and detected_map.surface[self.x - 1][self.y] == 0:
                self.x = self.x - 1
        if self.x < 19:
            if pressed_keys[K_DOWN] and detected_map.surface[self.x + 1][self.y] == 0:
                self.x = self.x + 1

        if self.y > 0:
            if pressed_keys[K_LEFT] and detected_map.surface[self.x][self.y - 1] == 0:
                self.y = self.y - 1
        if self.y < 19:
            if pressed_keys[K_RIGHT] and detected_map.surface[self.x][self.y + 1] == 0:
                self.y = self.y + 1

    def map_with_drone(self, map_image):
        drona = pygame.image.load("assets/images/drona.png")
        map_image.blit(drona, (self.y * 20, self.x * 20))

        return map_image
