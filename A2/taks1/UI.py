import pygame

from Controller import Controller
from domain.constants import WHITE, MAP_WIDTH, PATH_GENERATION_STEPS, MAP, COLOR_PAIRS


class UI:
    def __init__(self):
        self.__controller = Controller()

    @staticmethod
    def __initialize_pygame():
        pygame.init()
        # load and set the logo
        logo = pygame.image.load("assets/images/logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Path in simple environment")

    def run(self):
        # initialize the pygame module
        self.__initialize_pygame()

        # create a surface on screen that has the size of 800 x 400
        screen = pygame.display.set_mode((len(self.__controller.algorithms) * MAP_WIDTH, 400))
        screen.fill(WHITE)

        # load the map
        self.__controller.load_map(MAP)
        # self.__controller.load_map()

        # compute the path's start and end
        (start_x, start_y), (end_x, end_y) = self.__controller.generate_path(PATH_GENERATION_STEPS)
        print()
        print("Start: " + str((start_x, start_y)))
        print("End: " + str((end_x, end_y)))

        # run the algorithms
        width_factor = 0
        for algorithm in self.__controller.algorithms:
            path, time = self.__controller.search_path(algorithm, start_x, start_y, end_x, end_y)

            print('-' * 20)
            print('Algorithm: ' + algorithm)
            if len(path) == 0:
                print("Path: doesn't exist")
                continue
            print('Time: ' + str(time))
            print('Path:\n' + str(path))
            print('-' * 20)

            walls_color, path_color = COLOR_PAIRS[width_factor % len(COLOR_PAIRS)]
            # print("color pair: ", str(walls_color), str(path_color)) # debug print
            screen.blit(self.__controller.display_with_path(walls_color, path_color, path), (width_factor * MAP_WIDTH, 0))
            width_factor += 1

        pygame.display.flip()

        # main loop
        while True:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
