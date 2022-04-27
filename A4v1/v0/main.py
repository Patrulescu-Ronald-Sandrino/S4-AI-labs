

def main():
    print("hello, world!")


if __name__ == "__main__":
    main()


# TODO
#   1. reposition drone so it doesn't start on a wall (see A3)
#   2.


""" 
Ideas (importance: 0 - very, 1 - medium, 2 - low):

importance 0:
    1. 
    2. 

importance 1:
    1. UI: add 3 ways to set the environment:
        1. default
        2. from file
        3. manual input
    2. UI: enable Run option in menu if the environment was set
    3. Map Manager: random, load, save, view, view as texttable
        + set the new the map
            -> (implies): repositioning the drone so it doesn't hit a wall
    
importance 2:
    1. replace conditions in Position.__init__() with:
        if tools.math.out_of_range(x, 0, MAX_INT - 1):
            ...
        if tools.math.out_of_range(y, 0, MAX_INT - 1):
            ...
    2. 

"""

"""
Things to keep:
    1. raise ValueError("[error][{}.{}()] {}\n".format(__class__, inspect.stack()[0].function, ""))
    2. sys.stderr.write("[warn][{}.{}()] {}\n".format(__class__, inspect.stack()[0].function, ""))
"""