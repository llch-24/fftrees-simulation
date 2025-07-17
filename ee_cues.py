import numpy as np
import pandas as pd
import random
import itertools
import matplotlib.pyplot as plt
from calculations import choose_add, choose_mult, u, add, mult

def compute_cues(g):
    A, B = g
    # basic additive cues
    m = (A + B) / 2
    cues = {
        'max':            max(A, B),
        'min':            min(A, B),
        'range':          abs(A - B),
        'mean':           m,
        'signs_diff':     int((A > 0 and B < 0) or (A < 0 and B > 0)),
        'both_positive':  int(A > 0 and B > 0),
        'both_negative':  int(A < 0 and B < 0),
        'count_positive': int(A > 0) + int(B > 0),
        'count_negative': int(A < 0) + int(B < 0),
    }

    # multiplicative‐style cues (for factors)
    if A > 0 and B > 0:
        cues.update({
            'both_gainers':   int(A > 1   and B > 1),
            'both_shrinkers': int(A < 1   and B < 1),
            'count_gainers':  int(A > 1) + int(B > 1),
            'count_shrinkers':int(A < 1) + int(B < 1),
        })

    return cues


def add_update(x, gamble, branch):
    """
    given wealth x (in additive gamble),
    branch=1 → +A; branch=2 → +B.
    """
    A, B = gamble
    return x + (A if branch == 1 else B)

def mult_update(x, gamble, branch):
    """
    given wealth x (in multiplicative gamble),
    branch=1 → *f1; branch=2 → *f2.
    """
    f1, f2 = gamble
    return x * (f1 if branch == 1 else f2)

def simulate_ee_dataset(
    initial_wealth: float,
    gambles: list,
    chooser_fn,
    updater_fn,
    n_rounds: int,
    eta: float,  # set to 0 for additive, 1 for multiplicative EE
    dynamic: str = "additive"
) -> pd.DataFrame:
    x = initial_wealth
    x_chained = initial_wealth
    records = []

    for r in range(1, n_rounds + 1):
        g1, g2 = random.sample(gambles, 2)
        choice = chooser_fn(x, g1, g2, eta)
        chosen = g1 if choice == 1 else g2

        # One-step expected wealth
        if updater_fn is add_update:
            x_chained += 0.5 * (chosen[0] + chosen[1])
        else:
            x_chained *= 0.5 * (chosen[0] + chosen[1])

        # Realized outcome
        branch = 1 if random.random() < 0.5 else 2
        x_next = updater_fn(x, chosen, branch)
        realized = chosen[branch - 1]

        # Compute cues for both gambles
        cues_g1 = compute_cues(g1)
        cues_g2 = compute_cues(g2)

        row = {
            'round': r,
            'g1_a': g1[0],
            'g1_b': g1[1],
            'g2_a': g2[0],
            'g2_b': g2[1],
            'ee_choice': choice,
            'coin_flip': branch,
            'realized': realized,
            'wealth_expected': x_chained,
            'wealth_actual': x_next
        }

        # Add all cue features
        row.update({f"g1_{k}": v for k, v in cues_g1.items()})
        row.update({f"g2_{k}": v for k, v in cues_g2.items()})

        records.append(row)
        x = x_next

    return pd.DataFrame(records)

additive_changes = [-407.0, -305.5, -241.5, -49.0, 108.5, 210.5, 309.5, 440.5, 0.0]
multiplicative_factors = [0.427, 0.583, 0.649, 0.841, 1.006, 1.184, 1.446, 1.739, 2.164]

add_gambles = list(itertools.combinations(additive_changes, 2))
mult_gambles = list(itertools.combinations(multiplicative_factors, 2))

n_trials = 1000
initial_wealth = 1000

# Additive EE (eta = 0)
df_add = simulate_ee_dataset(
    initial_wealth=initial_wealth,
    gambles=add_gambles,
    chooser_fn=choose_add,
    updater_fn=add_update,
    n_rounds=n_trials,
    eta=0,
    dynamic='additive'
)
df_add.to_csv("ee_additive_dataset.csv", index=False)
print("Saved ee_additive_dataset.csv")

# Multiplicative EE (eta = 1)
df_mult = simulate_ee_dataset(
    initial_wealth=initial_wealth,
    gambles=mult_gambles,
    chooser_fn=choose_mult,
    updater_fn=mult_update,
    n_rounds=n_trials,
    eta=1,
    dynamic='multiplicative'
)
df_mult.to_csv("ee_multiplicative_dataset.csv", index=False)
print("Saved ee_multiplicative_dataset.csv")