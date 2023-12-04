import os

import matplotlib.pylab as plt
import pandas as pd
import seaborn as sns

# Inputs
PATH_TVL_HISTORY = "../data/raw/tvl-history.csv"
# Outputs
PATH_PLOT_TVL = "../results/plots/tvl-history.png"


def main():
    tvl_history = pd.read_csv(PATH_TVL_HISTORY, sep=",")

    data = []
    for index, row in tvl_history.iterrows():
        timestamp = row["timestamp"]
        tvl = row["tvlUSD"] / 1000000000
        data.append([timestamp, tvl])
    df = pd.DataFrame(data, columns=['time', 'tvl_usd'])

    sns.set_theme()

    fig_dims = (10, 4)
    fig, ax = plt.subplots(figsize=fig_dims)

    ax = sns.lineplot(data=df, x="time", y="tvl_usd", ax=ax).set_title('Total Value Locked (USD)')
    ax = plt.gca()
    xticks = ax.get_xticks()
    ax.set_xticklabels([pd.to_datetime(tm, unit='s').strftime('%Y-%m-%d') for tm in xticks], rotation=0)
    ax.tick_params(labelsize=10)
    ax.set_ylabel('')
    ax.set_xlabel('')
    ax.yaxis.set_major_formatter('{x:1.0f}B')

    os.makedirs(os.path.dirname(PATH_PLOT_TVL), exist_ok=True)
    ax.figure.savefig(PATH_PLOT_TVL, bbox_inches="tight")


if __name__ == '__main__':
    main()
