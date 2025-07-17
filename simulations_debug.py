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

def simulate(
    initial_wealth: float,
    gambles: list,
    chooser_fn,
    updater_fn,
    n_rounds: int,
    eta: float
) -> pd.DataFrame:
    # actual wealth
    x = initial_wealth
    # expected wealth
    x_chained = initial_wealth
    records = []

    for r in range(1, n_rounds+1):
        # pick two gambles at random
        g1, g2 = random.sample(gambles, 2)

        # chooser_fn returns 1 or 2
        branch_choice = chooser_fn(x, g1, g2, eta)

        # figure out which tuple was chosen
        chosen = g1 if branch_choice == 1 else g2

        # compute expected next-wealth 
        if updater_fn is add_update:
            x_chained = x_chained + 0.5*(chosen[0] + chosen[1])
            
        else:
            x_chained = x_chained * 0.5*(chosen[0] + chosen[1])

        # simulate coin-flip outcome --> which branch from chosen gamble is realized
        branch_real = 1 if random.random() < 0.5 else 2
        x_next = updater_fn(x, chosen, branch_real)

        # record everything
        records.append({
            'round': r,
            'g1': g1,
            'g2': g2,
            'choice': branch_choice,
            'wealth_actual': x_next,
            'coin_flip': branch_real,
            'wealth_expected': x_chained
        })

        # wealth for next round
        x = x_next

    # df w columns 
    # ['round','g1','g2','choice','wealth_actual','wealth_expected']
    return pd.DataFrame(records)

### ADDITIVE DYNAMIC ####
eta_list = [0.25, 0.5, 0.75, 1.0, 1.5]
n_rounds = 100

for eta in eta_list:
    df = simulate(
        initial_wealth=1000,
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

    fig, ax = plt.subplots()

    ax.plot(
        df['round'],
        df['wealth_expected'],   
        label='Expected (one‐step)'
    )

    ax.plot(
        df['round'],
        df['wealth_actual'],
        linestyle='--',
        alpha=0.6,
        label='Actual'
    )

    ax.set_title(f'Additive Dynamic: η = {eta:.2f} (n={n_rounds})')
    ax.set_xlabel('Round')
    ax.set_ylabel('Wealth')
    ax.legend()

    png_name = f'additive_plot_eta_{eta:.2f}.png'
    # plt.tight_layout()
    plt.savefig(png_name, dpi=300)
    print(f'Saved plot to {png_name}')
    plt.close(fig)

### MULTIPLICATIVE DYNAMIC ####
import cProfile
import pstats

if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()

    # Run your full script logic here
    ### ADDITIVE DYNAMIC ####
    eta_list = [0.25, 0.5, 0.75, 1.0, 1.5]
    n_rounds = 100

    for eta in eta_list:
        df = simulate(
            initial_wealth=1000,
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

        fig, ax = plt.subplots()
        ax.plot(df['round'], df['wealth_expected'], label='Expected (one‐step)')
        ax.plot(df['round'], df['wealth_actual'], linestyle='--', alpha=0.6, label='Actual')
        ax.set_title(f'Additive Dynamic: η = {eta:.2f} (n={n_rounds})')
        ax.set_xlabel('Round')
        ax.set_ylabel('Wealth')
        ax.legend()
        png_name = f'additive_plot_eta_{eta:.2f}.png'
        plt.savefig(png_name, dpi=300)
        print(f'Saved plot to {png_name}')
        plt.close(fig)

    ### MULTIPLICATIVE DYNAMIC ####
    for eta in eta_list:
        df = simulate(
            initial_wealth=1000,
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

        fig, ax = plt.subplots()
        ax.plot(df['round'], df['wealth_expected'], label='Expected (one‐step)')
        ax.plot(df['round'], df['wealth_actual'], linestyle='--', alpha=0.6, label='Actual')
        ax.set_title(f'Multiplicative Dynamic: η = {eta:.2f} (n={n_rounds})')
        ax.set_xlabel('Round')
        ax.set_ylabel('Wealth')
        ax.legend()
        png_name = f'multiplicative_plot_eta_{eta:.2f}.png'
        plt.savefig(png_name, dpi=300)
        print(f'Saved plot to {png_name}')
        plt.close(fig)

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats(20)  # adjust number to see more/less functions
