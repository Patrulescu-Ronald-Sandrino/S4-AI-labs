# -*- coding: utf-8 -*-
"""
In this file your task is to write the solver function!

"""
from typing import Dict, Any, Optional, Tuple

THETA_SETS = {
    "PVB": (25, 40, None),
    "PB": (10, 25, 40),
    "P": (0, 10, 20),
    "ZO": (-5, 0, 5),
    "N": (-20, -10, 0),
    "NB": (-40, -25, -10),
    "NVB": (None, -40, -25),
}

OMEGA_SETS = {
    "PB": (3, 8, None),
    "P": (0, 3, 6),
    "ZO": (-1, 0, 1),
    "N": (-6, -3, 0),
    "NB": (None, -8, -3),
}

F_SETS = {
    "NVVB": (None, -32, -24),
    "NVB": (-32, -24, -16),
    "NB": (-24, -16, -8),
    "N": (-16, -8, 0),
    "Z": (-4, 0, 4),
    "P": (0, 8, 16),
    "PB": (8, 16, 24),
    "PVB": (16, 24, 32),
    "PVVB": (24, 32, None),
}

FUZZY_TABLE = {  # FUZZY_TABLE[<theta>][<omega>]
    # "" : {"PB": "", "P": "", "ZO": "", "N": "", "NB": ""},
    "PVB": {"PB": "PVVB", "P": "PVVB", "ZO": "PVB", "N": "PB", "NB": "P"},
    "PB": {"PB": "PVVB", "P": "PVB", "ZO": "PB", "N": "P", "NB": "Z"},
    "P": {"PB": "PVB", "P": "PB", "ZO": "P", "N": "Z", "NB": "N"},
    "ZO": {"PB": "PB", "P": "P", "ZO": "Z", "N": "N", "NB": "NB"},
    "N": {"PB": "P", "P": "Z", "ZO": "N", "N": "NB", "NB": "NVB"},
    "NB": {"PB": "Z", "P": "N", "ZO": "NB", "N": "NVB", "NB": "NVVB"},
    "NVB": {"PB": "N", "P": "NB", "ZO": "NVB", "N": "NVVB", "NB": "NVVB"}
}


def fuzzify(x: float, start: Optional[float], peak: float, end: Optional[float]) -> float:
    result: float = 1

    if start is not None:
        result = min(result, (x - start)/(peak - start))
    if end is not None:
        result = min(result, (end - x)/(end - peak))

    return max(result, 0)


def get_memberships(x: float, sets: Dict[str, Tuple[Optional[float], float, Optional[float]]]):
    return {key: fuzzify(x, *sets[key]) for key in sets.keys()}


def print_double_dict(dict_: Dict[Any, Dict[Any, Any]]):
    for key1 in dict_.keys():
        print(f'{key1}: {dict_[key1]}')


def solver(t, w):
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

    # compute membership degrees of the angle t and the angular speed w
    # t, w = 7, -0.5
    theta_memberships = get_memberships(t, THETA_SETS)
    omega_memberships = get_memberships(w, OMEGA_SETS)
    # print(theta_memberships)
    # print(omega_memberships)


    # compute the membership degrees for F
    # 1-liner variant
    # f_memberships = {theta_set: {omega_set: min(theta_memberships[theta_set], omega_memberships[omega_set]) for omega_set in OMEGA_SETS.keys()} for theta_set in THETA_SETS.keys()}
    # print(f_memberships)

    # non 1-liner variant
    # f_memberships = {}
    # for theta_set in THETA_SETS.keys():
    #     f_memberships[theta_set] = {}
    #     for omega_set in OMEGA_SETS.keys():
    #         f_memberships[theta_set][omega_set] = min(theta_memberships[theta_set], omega_memberships[omega_set])
    # print(f_memberships)
    # print_double_dict(f_memberships)

    # compute the membership degree for each F class
    f_classes_memberships = {f_set: -1 for f_set in F_SETS}
    # doesn't work
    # f_classes_memberships = {FUZZY_TABLE[theta_set][omega_set]: max(f_classes_memberships[FUZZY_TABLE[theta_set][omega_set]], min(theta_memberships[theta_set], omega_memberships[omega_set])) for theta_set in THETA_SETS.keys() for omega_set in OMEGA_SETS.keys()}
    # f_classes_memberships = {FUZZY_TABLE[theta_set][omega_set]: max(f_classes_memberships[FUZZY_TABLE[theta_set][omega_set]], min(theta_memberships[theta_set], omega_memberships[omega_set])) for theta_set, omega_set in ((x, y) for x in THETA_SETS.keys() for y in OMEGA_SETS.keys())}

    for theta_set in THETA_SETS.keys():
        for omega_set in OMEGA_SETS.keys():
            f_classes_memberships[FUZZY_TABLE[theta_set][omega_set]] = max(f_classes_memberships[FUZZY_TABLE[theta_set][omega_set]], min(theta_memberships[theta_set], omega_memberships[omega_set]))
    # print(f_classes_memberships)

    # de-fuzzify the results for F
    numerator: float = sum(f_classes_memberships[key] * F_SETS[key][1] for key in f_classes_memberships.keys())
    denominator: float = sum(f_classes_memberships[key] for key in f_classes_memberships.keys())
    f: Optional[float] = numerator/denominator if denominator != 0 else None
    # print(f'f={numerator}/{denominator}={f}')

    return f
