from controller import Controller
from repository import Repository
from ui import UI


def main():
    repository = Repository()
    controller = Controller(repository)
    UI(controller).run()


if __name__ == "__main__":
    main()


"""
TODO:
1. Service: {load,save}_map - deal with different FileSystems (paths on Linux vs Window) 

Ideas:
    1. design a class called GUIConfigs which is passed to GUI.__init__() instead of having 15000 parameters



Sources:
    - enumeration (access the index in a 'for' loop) https://stackoverflow.com/questions/11475748/loop-through-list-with-both-content-and-index
    - getter property https://www.geeksforgeeks.org/getter-and-setter-in-python/
    - math - floor: math.floor(number) https://www.w3schools.com/python/ref_math_floor.asp
    - math - log: math.log(number, base=e) https://www.geeksforgeeks.org/log-functions-python/
    - override array subscript operator https://stackoverflow.com/questions/1957780/how-to-override-the-operator-in-python
    - pass methods as arguments https://www.studytonight.com/python-howtos/how-to-pass-a-method-as-an-argument-in-python
    - static instances of a class https://stackoverflow.com/questions/2546608/create-static-instances-of-a-class-inside-said-class-in-python
    - static typing first answer from https://stackoverflow.com/questions/3933197/how-to-declare-variable-type-c-style-in-python
    - string format: "{name} has {} apples".format(number_of_apples, name="Andrei") https://www.w3schools.com/python/ref_string_format.asp
    - texttable
        1. https://www.geeksforgeeks.org/texttable-module-in-python/
        2. ValueError: max_width too low to render data - first answer https://stackoverflow.com/questions/24507288/python-printing-a-list-as-a-table-using-texttable
    - type hints
        1. first answer https://stackoverflow.com/questions/37835179/how-can-i-specify-the-function-type-in-my-type-hints
            1. https://peps.python.org/pep-0483/#fundamental-building-blocks
        2. first answer https://stackoverflow.com/questions/2489669/how-do-python-functions-handle-the-types-of-parameters-that-you-pass-in
    - type hints - forward references https://peps.python.org/pep-0484/#forward-references

"""