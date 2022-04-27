import os.path
from typing import Tuple, Dict

import pygame

from domain.map import Map
from tools.visual import Color


BLOCK_SIZE: int = 20


class GUI:
    def __init__(self, map_: Map, path: Dict[Tuple[int, int], int]):
        self.__map: Map = map_
        self.__path: Dict[Tuple[int, int], int] = path

        self.assets_folder: str = 'assets'
        self.drone_image: str = 'drone.png'

    @staticmethod
    def init_pygame(dimension: Tuple[int, int]):
        pygame.init()

        pygame.display.set_caption("A4")
        # pygame.display.set_icon(pygame.image.load('path/to/window/icon'))

        screen = pygame.display.set_mode(dimension)
        screen.fill(Color.WHITE)
        return screen

    def handle_events(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    # if pygame.key == pygame.K_r:
                    if event.key == pygame.K_r:
                        print("[log] R key pressed")
                        self.run()
                        raise Exception("Re-run")

    def get_drone_image(self):
        return pygame.image.load(os.path.join(os.path.curdir, self.assets_folder, self.drone_image))

    @staticmethod
    def get_map_image(map_: Map, background_color: Tuple[int, int, int], wall_color: Tuple[int, int, int]):
        map_image = pygame.Surface((map_.rows * BLOCK_SIZE, map_.columns * BLOCK_SIZE))
        wall_block = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))

        map_image.fill(background_color)
        wall_block.fill(wall_color)

        for row in range(map_.rows):
            for column in range(map_.columns):
                if map_.surface[row][column] == Map.CellType.WALL:
                    map_image.blit(wall_block, (column * BLOCK_SIZE, row * BLOCK_SIZE))

        return map_image

    def run(self, speed: float = 0.5):
        print('Starting GUI! Press R to restart drawing it.')
        pygame.font.init()
        FONT = pygame.font.SysFont('comicsansms', 15, True)
        pygame.font.quit()

        screen = GUI.init_pygame((self.__map.rows * BLOCK_SIZE, self.__map.columns * BLOCK_SIZE))
        screen.blit(GUI.get_map_image(self.__map, Color.WHITE, Color.BLUE), (0, 0))
        pygame.display.update()
        self.handle_events()
        pygame.quit()

        if len(self.__path) == 0:
            self.quit()
            return

        screen = GUI.init_pygame((self.__map.rows * BLOCK_SIZE, self.__map.columns * BLOCK_SIZE))

        for (row, column), energy in self.__path.items():
            try:
                self.handle_events()
            except Exception:
                return

            screen.blit(GUI.get_map_image(self.__map, Color.WHITE, Color.BLUE), (0, 0))
            # TODO

            # screen.blit(FONT.render(text, True, Color.WHITE), (column * BLOCK_SIZE + 5, row * BLOCK_SIZE)) # TODO: display sensors' numbers
            pygame.display.update()

        self.handle_events()

    @staticmethod
    def quit():
        pygame.quit()
