import numpy as np
import itertools
import pandas as pd
import random

print("main.py is working!!")

#starting wealth
x0 = 1000 


def u(x, eta): 
    """
    Iso-elastic function:
    * if eta != 1, u(x) = (x^(1-eta) - 1) / (1 - eta)
    * if eta = 1, u(x) = log(x) #risk averse

    """
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
    A, B = gamble #define A and B

    # initial/prior wealth state
    base = u(x, eta)

    # define utility of A and B
    uA = u(x+A, eta) 
    uB = u(x+B, eta)
    return 0.5*(uA - base) + 0.5*(uB - base)

# decision rule for additive case
def choose_eut_add(x, g1, g2, eta):
    """
    compare g1(a1, b1) to g2(a2, b2)
    choose g1 if > g2, else choose g2

    """
    eu1 = add(x, g1, eta)
    eu2 = add(x, g2, eta) # need to define gambles
    return 1 if eu1 > eu2 else 2

def mult(x, gamble, eta):
    """
    compute EUT of one gamble in multiplicative scenario:
    * 50% chance of x*f1
    * 50% chance of x*f2

    """
    f1, f2 = gamble #define f1 and f2
    base = u(x, eta)
    uf1 = u(x*f1, eta)
    uf2 = u(x*f2, eta)
    return 0.5*(uf1 - base) + 0.5*(uf2 - base)

def choose_eut_mult(x, g1, g2, eta):
    """
    compare g1(f1, f2) to g2(f3, f4)
    choose g1 if > g2, else choose g2

    """
    eu1 = mult(x, g1, eta)
    eu2 = mult(x, g2, eta) # again, need to define gambles
    return 1 if eu1 > eu2 else 2

# def ee_add(x, gamble, eta):
#     """
#     compute EE optimal growth rate gamble in additive scenario:
#     * 50% chance of x + A
#     * 50% chance of x + B
#     where eta = 0 and u(x) = x

#     """
#     A, B = gamble
#     base = u(x, eta)
#     return 0.5*u((x + A, eta)) - base + 0.5*u((x + B, eta) - base)

def choose_ee_add(x, g1, g2, eta = 0):
    """
    compare g1(a1, b1) to g2(a2, b2)
    choose g1 if > g2, else choose g2
    
    """
    eu1 = add(x, g1, eta)
    eu2 = add(x, g2, eta) #define gambles
    return 1 if eu1 > eu2 else 2

# def ee_mult(x, gamble, eta):
#     """
#     compute EE optimal growth rate gamble in multiplicative scenario:
#     * 50% chance of x*f1
#     * 50% chance of x*f2
#     where eta = 1 and u(x) = ln(x)
    
#     """
#     f1, f2 = gamble # define gamble numbers
#     base = u(x, eta)
#     return 0.5*u((x + f1, eta)) - base + 0.5*u((x + f2, eta) - base)

def choose_ee_mult(x, g1, g2, eta = 1):
    """
    compare g1(f1, f2) to g2(f3, f4)
    choose g1 if > g2, else choose g2

    """
    eu1 = mult(x, g1, eta)
    eu2 = mult(x, g2, eta)
    return 1 if eu1 > eu2 else 2


### SIMULATION! ###  

additive_changes = [-407.0, -305.5, -241.5, -49.0, 108.5, 210.5, 309.5, 440.5, 0.0] # gamble factors from the paper -- should I come up w my own?
multiplicative_factors = [0.427, 0.583, 0.649, 0.841, 1.006, 1.184, 1.446, 1.739, 2.164]

# create unique tuples 
additive_gambles = list(itertools.combinations(additive_changes, 2))
multiplicative_gambles = list(itertools.combinations(multiplicative_factors, 2))

def simulate_all(x0=1000, eta=1.25): # assume η = 1.25 to reflect moderate risk aversion, between lit's 1 and 1.5 estimates
    """
    attempting to simulate over all unordered pairs of gambles (as defined above)
    return DF w each row being one unique (g1, g2) combination
    
    """
    records = []
    for g1, g2 in itertools.combinations(additive_gambles, 2):
        eut_choice = choose_eut_add(x0, g1, g2, eta)
        ee_choice  = choose_ee_add(x0, g1, g2)  # eta=0 
        records.append({
            'mode': 'add',
            'g1': g1,
            'g2': g2,
            'EUT': eut_choice,
            'EE': ee_choice,
        })

    for g1, g2 in itertools.combinations(multiplicative_gambles, 2):
        eut_choice = choose_eut_mult(x0, g1, g2, eta)
        ee_choice  = choose_ee_mult(x0, g1, g2)  # eta=1 
        records.append({
            'mode': 'mult',
            'g1': g1,
            'g2': g2,
            'EUT': eut_choice,
            'EE': ee_choice,
        })
    return pd.DataFrame(records)

df = simulate_all()

print(df.shape)
print(df.columns)
print(df.head())
print(df.tail())
print(df.describe())

print("EUT value counts:\n", df['EUT'].value_counts())
print("EE  value counts:\n", df['EE'].value_counts())



# # tests
# if __name__ == "__main__":
#     # test the utility‐function
#     for eta in [0, 0.5, 1, 2]:
#         result = u(x0, eta)
#         print(f"u({x0}, eta={eta}) = {result:.4f}")

#     # test the choice‐rule for additive
#     x0 = 1000
#     eta = 1
#     g1 = (11, -2)
#     g2 = (-1.3, 8)
#     choice = choose_eut_add(x0, g1, g2, eta)
#     choice2 = choose_ee_add(x0, g1, g2, eta)
#     print("Choose additive gamble EUT:", choice)
#     print("EE:", choice2)

#     # test the choice‐rule for multiplicative
#     x0 = 1000
#     eta = 0
#     g1 = (3, 1.3)
#     g2 = (4.4, 0.01)
#     choice = choose_eut_mult(x0, g1, g2, eta)
#     choice2 = choose_ee_mult(x0, g1, g2, eta)
#     print("Choose multiplicative gamble EUT:", choice)
#     print("EE:", choice2)


# some other thoughts on simulation

#     def simulate_gamble_choices_eu_vs_ee(A, B, C, D):
#         # test the choice‐rule for multiplicative
#         x0 = 1000
#         eta = 0
#         g1 = (A, B)
#         g2 = (C, D)
#         choice = choose_eut_mult(x0, g1, g2, eta)
#         choice2 = choose_ee_mult(x0, g1, g2, eta)
#         print(f"(A, B, C, D): ({A}, {B}, {C}, {D})")
#         print("EUT Choice:", choice)
#         print("EE Choice:", choice2)


#     list_of_As = []
#     list_of_Bs = []
#     list_of_Cs = []
#     list_of_Ds = []

#     for i in range(10):
#         import random
#         # list_of_As.append(random.randint(1, 10))
#         list_of_As.append(5)
#         list_of_Bs.append(random.randint(1, 10))
#         list_of_Cs.append(random.randint(1, 10))
#         list_of_Ds.append(random.randint(1, 10))

#     print(list_of_As)
#     print(list_of_Bs)
#     print(list_of_Cs)
#     print(list_of_Ds)

#     for i in range(len(list_of_As)):
#         simulate_gamble_choices_eu_vs_ee(list_of_As[i], list_of_Bs[i], list_of_Cs[i], list_of_Ds[i])