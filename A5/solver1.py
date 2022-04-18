# -*- coding: utf-8 -*-
"""
In this file your task is to write the solver function!

"""

class Shape:
    def __int__(self):
        pass

    def com

def solver(t,w):
    """
    Parameters
    ----------
    t : TYPE: float
        DESCRIPTION: the angle theta
    w : TYPE: float
        DESCRIPTION: the angular speed omega

    Returns
    -------
    F : TYPE: float
        DESCRIPTION: the force that must be applied to the cart
    or
    
    None :if we have a division by zero

    """

    ANGLE_SETS = {
        "NVB": (None, -40, -25),
          "NB": (-40, -25, -10),
          "N": (-20, -10, 0),
          "ZO": (-5, 0, 5),
          "P": (0, 10, 20),
          "PB": (10, 25, 40),
          "PVB": (25, 40, None),
                  }

    SPPED_SETS = {"NB": (-40, -25, -10),
                  "N": (-20, -10, 0),
                  "ZO": (-5, 0, 5),
                  "P": (0, 10, 20),
                  "PB": (10, 25, 40),
                  "PVB": (25, 40, None),
                  }

    return None

