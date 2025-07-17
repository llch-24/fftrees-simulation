import numpy as np
import itertools
import pandas as pd
import random
import matplotlib.pyplot as plt

def u(x, eta): 
    """
    Iso-elastic function:
    * if eta != 1, u(x) = (x^(1-eta) - 1) / (1 - eta)
    * if eta = 1, u(x) = log(x) #risk averse

    """   
    if x <= 0:
        return -np.inf         # treat zero‐or‐negative as “bankrupt”
    if eta == 1:
        return np.log(x)
    return x**(1-eta) / (1-eta)

# Calculation for each scenario --> we calculate the expected value for each gamble 
def add(x, gamble, eta):
    """
    compute EUT of one gamble in additive scenario:
    * 50% chance of x + A
    * 50% chance of x + B

    """
    A, B = gamble
    base = u(x, eta)
    uA = u(x+A, eta) 
    uB = u(x+B, eta)
    return 0.5*(uA - base) + 0.5*(uB - base)

def mult(x, gamble, eta):
    """
    compute EUT of one gamble in multiplicative scenario:
    * 50% chance of x*f1
    * 50% chance of x*f2

    """
    f1, f2 = gamble
    base = u(x, eta)
    uf1 = u(x*f1, eta)
    uf2 = u(x*f2, eta)
    return 0.5*(uf1 - base) + 0.5*(uf2 - base)

def choose_add(x, g1, g2, eta):
    return 1 if add(x, g1, eta) > add(x, g2, eta) else 2

def choose_mult(x, g1, g2, eta):
    return 1 if mult(x, g1, eta) > mult(x, g2, eta) else 2
