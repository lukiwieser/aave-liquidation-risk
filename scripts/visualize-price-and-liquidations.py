import os

import dateutil.parser as dp
import matplotlib.pylab as plt
import pandas as pd
import seaborn as sns

# Inputs
PATH_PRICE_HISTORY = "../data/raw/price-history/ETH-USD.csv"
PATH_TX_HISTORY_LENDING_POOL_V2 = "../data/parsed/tx-history_lending-pool-v2.csv"
# Outputs
PATH_PRICE_CHART = "../results/plots/price-chart.png"


def main():
    price_history = pd.read_csv(PATH_PRICE_HISTORY, sep=",")
    tx_history = pd.read_csv(PATH_TX_HISTORY_LENDING_POOL_V2, sep=";")

    liquidation_timestamps = tx_history[tx_history["input_decoded"].str.contains("liquidationCall")][
        "timestamp"].tolist()

    price_history["time"] = price_history.apply(lambda row: dp.parse(row["date"]).timestamp(), axis=1)
    price_history["price"] = price_history.apply(lambda row: (row["high"] + row["low"]) / 2, axis=1)

    # plot
    sns.set_theme()
    fig, axs = plt.subplots(nrows=2, ncols=1, sharex=True, height_ratios=[2, 1])
    fig.suptitle('Ethereum Price and Liquidations')
    # price:
    sns.lineplot(data=price_history, x="time", y="price", ax=axs[0])
    axs[0].set_ylabel("Ethereum Price (in USD)")
    axs[0].set_ylim(0, 4500)
    # liquidations:
    sns.stripplot(x=liquidation_timestamps, alpha=.5, ax=axs[1], jitter=0.3)
    axs[1].set_ylabel("Liquidations")
    # x-axis
    xticks = axs[1].get_xticks()
    axs[1].set_xticklabels([pd.to_datetime(tm, unit='s').strftime('%Y-%m-%d') for tm in xticks], rotation=90)
    axs[1].tick_params(labelsize=10)

    os.makedirs(os.path.dirname(PATH_PRICE_CHART), exist_ok=True)
    fig.savefig(PATH_PRICE_CHART, bbox_inches="tight")


if __name__ == '__main__':
    main()
