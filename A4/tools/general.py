import inspect


def function_name():
    return inspect.stack()[1].function
