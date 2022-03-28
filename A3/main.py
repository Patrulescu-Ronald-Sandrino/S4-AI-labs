from controller import Controller
from ui import UI


def main():
    controller = Controller(None)
    UI(controller).run()


if __name__ == "__main__":
    main()


"""




Sources:
    - enumeration (access the index in a 'for' loop) https://stackoverflow.com/questions/11475748/loop-through-list-with-both-content-and-index
    - math - floor: math.floor(number) https://www.w3schools.com/python/ref_math_floor.asp
    - math - log: math.log(number, base=e) https://www.geeksforgeeks.org/log-functions-python/
    - override array subscript operator https://stackoverflow.com/questions/1957780/how-to-override-the-operator-in-python
    - pass methods as arguments https://www.studytonight.com/python-howtos/how-to-pass-a-method-as-an-argument-in-python
    - static instances of a class https://stackoverflow.com/questions/2546608/create-static-instances-of-a-class-inside-said-class-in-python
    - string format: "{name} has {} apples".format(number_of_apples, name="Andrei") https://www.w3schools.com/python/ref_string_format.asp
    - type hints
        1. first answer https://stackoverflow.com/questions/37835179/how-can-i-specify-the-function-type-in-my-type-hints
            1. https://peps.python.org/pep-0483/#fundamental-building-blocks
        2. first answer https://stackoverflow.com/questions/2489669/how-do-python-functions-handle-the-types-of-parameters-that-you-pass-in
    - type hints - forward references https://peps.python.org/pep-0484/#forward-references

"""