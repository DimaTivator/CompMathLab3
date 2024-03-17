import numpy as np
import math


def f1(x):
    return -3 * x ** 3 - 5 * x ** 2 + 4 * x - 2


def f2(x):
    return np.sin(x) ** 2 * np.cos(x)


def f3(x):
    if type(x) is float and x <= 1e-10:
        raise ValueError("x must be greater than 0")
    return 0.2 * x * np.log(x)


def f4(x):
    return 1 / x ** 2 * np.sin(x)


def f5(x):
    return 1 / np.sqrt(x ** 2 - 4)

