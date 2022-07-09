"""
@Project ：Microsat Engineering
@File ：TS_Formulas.py
@Author ：David Canosa Ybarra
@Date ：17/06/2022 14:39
"""

from math import pi

Boltzmann = 5.67 * 10 ** -8


def Power_E(Area, Temp_K, Boltzmann = Boltzmann):
    """
    :param Area: Surface area of the panel
    :param Temp_K: Temperature of the panel
    :param Boltzmann: constant
    :return: Power emitted by the panel
    """
    return 2 * Area * Boltzmann * Temp_K ** 4


def Power_R(Power_E, Area, Spacing):
    """
    :param Power_E: Emitted power from adjacent panel
    :param Area: Area of receiving panel
    :param Spacing: Spacing between the two panels
    :return: Power received by receiving panel
    """
    return Area * (Power_E / (4 * pi * Spacing ** 2))
