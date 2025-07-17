import numpy as np
import itertools
import pandas as pd
import random
import matplotlib.pyplot as plt
from calculations import choose_add, choose_mult

### SIMULATION! ###  

additive_changes = [-407.0, -305.5, -241.5, -49.0, 108.5, 210.5, 309.5, 440.5, 0.0]
multiplicative_factors = [0.427, 0.583, 0.649, 0.841, 1.006, 1.184, 1.446, 1.739, 2.164]
add_gambles = list(itertools.combinations(additive_changes, 2))
mult_gambles = list(itertools.combinations(multiplicative_factors, 2))

# apply outcomes of gamble coin toss
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


def simulate(
    initial_wealth: float,
    gambles: list,
    chooser_fn,
    updater_fn,
    n_rounds: int,
    eta: float
) -> pd.DataFrame:
    x = initial_wealth
    x_chained = initial_wealth
    records = []

    for r in range(1, n_rounds + 1):
        g1, g2 = random.sample(gambles, 2)
        choice = chooser_fn(x, g1, g2, eta)  # 1 or 2
        chosen = g1 if choice == 1 else g2

        # expected wealth update
        if updater_fn is add_update:
            x_chained += 0.5 * (chosen[0] + chosen[1])
        else:
            x_chained *= 0.5 * (chosen[0] + chosen[1])

        # Simulate the outcome of the gamble
        branch_real = 1 if random.random() < 0.5 else 2  # Coin flip
        x_next = updater_fn(x, chosen, branch_real)

        realized = chosen[branch_real - 1]

        # Compute cues for both gambles
        cues_g1 = compute_cues(g1)
        cues_g2 = compute_cues(g2)

        # Save all info for this round
        row= {
            'round': r,
            'g1': g1,
            'g2': g2,
            'choice': choice,                 # model's choice
            'coin_flip': branch_real,        # realized outcome
            'wealth_expected': x_chained,
            'wealth_actual': x_next,
            'realized': realized
        }


        row.update({f"g1_{k}": v for k, v in cues_g1.items()})
        row.update({f"g2_{k}": v for k, v in cues_g2.items()})

        records.append(row)
        x = x_next

    return pd.DataFrame(records)



### ADDITIVE DYNAMIC ####
eta_list = [0.25, 0.5, 0.75, 1.0, 1.5]
n_rounds = 800
initial = 1000

for eta in eta_list:
    df = simulate(
        initial_wealth=initial,
        gambles=add_gambles,
        chooser_fn=choose_add,
        updater_fn=add_update,
        n_rounds=n_rounds,
        eta=eta
    )

    df['eta'] = eta
    filename = f'additive_sim_eta_{eta:.2f}.csv'
    df.to_csv(filename, index=False)
    print(f'Wrote {filename}')

    # --- compute time-average growth curve ---
    t      = df['round'].values
    X_exp  = df['wealth_expected'].values
    X_act  = df['wealth_actual'].values
    d_time = df['realized'].mean()
    X_time = initial + d_time * t

    # --- plot all three curves ---
    fig, ax = plt.subplots()
    ax.plot(t,       X_exp,  label='Expected (one-step)')
    ax.plot(t,       X_act,  linestyle='--', alpha=0.6, label='Actual')
    ax.plot(t,       X_time, '-.',                  label='Time-avg growth')

    ax.set_title(f'Additive Dynamic: η = {eta:.2f} (n={n_rounds})')
    ax.set_xlabel('Round')
    ax.set_ylabel('Wealth')
    ax.legend()
    ax.grid(True, ls=':', alpha=0.5)

    png_name = f'additive_plot_eta_{eta:.2f}.png'
    plt.tight_layout()
    plt.savefig(png_name, dpi=300)
    print(f'Saved plot to {png_name}')
    plt.close(fig)

### MULTIPLICATIVE DYNAMIC ####
eta_list = [0.25, 0.5, 0.75, 1.0, 1.5]
n_rounds = 500
initial = 1000

for eta in eta_list:

    df = simulate(
        initial_wealth=initial,
        gambles=mult_gambles,
        chooser_fn=choose_mult,
        updater_fn=mult_update,
        n_rounds=n_rounds,
        eta=eta
    )

    df['eta'] = eta
    csv_name = f'multiplicative_sim_eta_{eta:.2f}.csv'
    df.to_csv(csv_name, index=False)
    print(f'Wrote {csv_name}')

    # --- compute time-average growth curve ---
    t      = df['round'].values
    X_exp  = df['wealth_expected'].values
    X_act  = df['wealth_actual'].values
    g_time = np.exp(np.log(df['realized']).mean())
    X_time = initial * (g_time ** t)

    # --- plot all three curves ---
    fig, ax = plt.subplots()
    ax.plot(t,       X_exp,  label='Expected (one-step)')
    ax.plot(t,       X_act,  linestyle='--', alpha=0.6, label='Actual')
    ax.plot(t,       X_time, '-.',                  label='Time-avg growth')

    ax.set_yscale('log')
    ax.set_title(f'Multiplicative Dynamic: η = {eta:.2f} (n={n_rounds})')
    ax.set_xlabel('Round')
    ax.set_ylabel('Wealth')
    ax.legend()
    ax.grid(True, which='both', linestyle=':', alpha=0.5)

    png_name = f'multiplicative_plot_eta_{eta:.2f}.png'
    plt.savefig(png_name, dpi=300)
    print(f'Saved plot to {png_name}')
    plt.close(fig)