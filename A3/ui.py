# -*- coding: utf-8 -*-


# imports
import math
from typing import Callable

import utils
from gui import *
from controller import *
from repository import *
from domain import *


# create a menu
#   1. map options:
#         a. create random map
#         b. load a map
#         c. save a map
#         d visualise map
#   2. EA options:
#         a. parameters setup
#         b. run the solver
#         c. visualise the statistics
#         d. view the drone moving on a path
#              function gui.movingDrone(currentMap, path, speed, markseen)
#              ATENTION! the function doesn't check if the path passes trough walls


class Command:
    def __init__(self, name: str, function: Callable[['UI'], None]):  # type hints; type hints - forward references
        self.__name = name
        self.__function = function

    def get_name(self) -> str:
        return self.__name

    def get_function(self) -> Callable[['UI'], None]:
        return self.__function


class Menu:
    def __init__(self, title: str):
        self.__title = title
        self.__commands = []

    def add(self, command: Command) -> 'Menu':
        # note: it returns Menu in order to be able to chain adds
        self.__commands.append(command)
        return self

    def __getitem__(self, key: str) -> Command:  # override array subscript operator
        try:
            return self.__commands[int(key)]
        except IndexError:
            pass
        except ValueError:
            pass
        return Command.INVALID

    def __str__(self) -> str:
        if len(self.__commands) == 0:
            return ""
        result = "\n\n{}:\n".format(self.__title)
        align = math.floor(math.log(max(len(self.__commands) - 1, 1), 10)) + 1  # math - log; math - floor
        for index, command in enumerate(self.__commands):  # enumeration (access the index in a 'for' loop)
            result += "\t{:>{align}}. {command}".format(index, align=align, command=command.get_name())  # string format
            if index < len(self.__commands) - 1:
                result += "\n"
        return result


class UI:
    def __init__(self, controller: Controller):
        self.__exit = False
        self.__controller = controller

    def _set_exit(self) -> None:
        self.__exit = True

    def run(self) -> None:
        self.__loop(Menu("Main Menu")
                    .add(Command.EXIT)
                    # .add(Command("Map Menu", lambda ui: ui.__loop()))
                    # .add(Command.EXIT)
                    .add((lambda menu_name: Command(menu_name, lambda ui: ui.__loop(Menu(menu_name)
                                                                                    .add(Command.EXIT)
                                                                                    .add(Command("Create random map",
                                                                                                 UI.__create_random_map))
                                                                                    .add(Command("Load map", UI.__load_map))
                                                                                    .add(Command("Save map", UI.__save_map))
                                                                                    .add(Command("Visualize map", UI.__visualize_map))
                                                                                    .add(Command.BACK)
                                                                                    )))("Map Menu"))
                    .add((lambda menu_name: Command(menu_name, lambda ui: ui.__loop(Menu(menu_name)
                                                                                    .add(Command.EXIT)
                                                                                    .add(Command("Parameters setup", UI.__parameters_setup))
                                                                                    .add(Command("Run the solver", UI.__run_solver))
                                                                                    .add(Command("Visualize the statistics", UI.__visualize_statistics))
                                                                                    .add(Command("View the drone moving on a path", UI.__view_drone_moving))
                                                                                    .add(Command.BACK)
                                                                                    )))("EA Menu"))
                    )

    def __loop(self, menu: Menu) -> None:
        # note that menu should be of type Menu
        while not self.__exit:
            print(menu)
            option = input("Your option: ")
            command = menu[option]
            # if command == Command.BACK:
            if id(command) == id(Command.BACK):
                return
            command.get_function()(self)

    def __create_random_map(self):
        not_implemented()
        # self.__controller.setMap(Map().random_map())

    def __load_map(self):
        not_implemented()

    def __save_map(self):
        not_implemented()

    def __visualize_map(self):
        not_implemented()

    def __parameters_setup(self):
        not_implemented()

    def __run_solver(self):
        not_implemented()

    def __visualize_statistics(self):
        not_implemented()

    def __view_drone_moving(self):
        not_implemented()


Command.EXIT = Command("Exit", UI._set_exit)  # pass methods as arguments
# Command.BACK = Command("Go back", utils.nop)  # static instances of a class
Command.BACK = Command("Go back", lambda ui: None)  # static instances of a class
Command.INVALID = Command("Invalid", lambda *args, **kwargs: print("Not an option!"))
