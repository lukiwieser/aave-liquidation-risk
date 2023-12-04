from argparse import ArgumentParser
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt
import matplotlib.ticker as ticker
import os

# Inputs
PATH_TX_HISTORY_LENDING_POOL_V2 = "../data/parsed/tx-history_lending-pool-v2.csv"
# Outputs
PATH_LIQUIDATION_CHART = "../results/plots/liquidation-chart.png"

def load_tx_history(file):
    df = pd.read_csv(file, sep=";") 
    return df

def main():
    tx_history = load_tx_history(PATH_TX_HISTORY_LENDING_POOL_V2)

    liquidations = []
    for index, row in tx_history.iterrows():
        if("liquidationCall" in row["input_decoded"]):
           liquidations.append(row["timestamp"])

    sns.set_theme()
    ax = sns.stripplot(x=liquidations, alpha=.5)
    ax = plt.gca()
    xticks = ax.get_xticks()
    ax.set_xticklabels([pd.to_datetime(tm, unit='s').strftime('%Y-%m-%d') for tm in xticks],rotation=50)
    ax.tick_params(labelsize=10)

    os.makedirs(os.path.dirname(PATH_LIQUIDATION_CHART), exist_ok=True)
    ax.figure.savefig(PATH_LIQUIDATION_CHART, bbox_inches="tight")

if __name__ == '__main__':
    main()