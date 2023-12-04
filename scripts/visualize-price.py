from argparse import ArgumentParser
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt
import matplotlib.ticker as ticker
import dateutil.parser as dp
import os

PATH_PRICE_HISTORY = "../data/raw/price-history/ETH-USD.csv"
PATH_PRICE_CHART = "../results/plots/price-chart.png"

def main():
    pricehistory = pd.read_csv(PATH_PRICE_HISTORY, sep=",")

    data =[]
    for index, row in pricehistory.iterrows():
        date = dp.parse(row["date"])
        timestamp =  date.timestamp()
        avg_price = (row["high"] + row["low"])/2
        data.append([timestamp,avg_price])
    df = pd.DataFrame(data, columns=['time', 'price'])

    sns.set_theme()
    ax = sns.lineplot(data=df, x="time", y="price")
    ax = plt.gca()
    xticks = ax.get_xticks()
    ax.set_xticklabels([pd.to_datetime(tm, unit='s').strftime('%Y-%m-%d') for tm in xticks],rotation=50)
    ax.tick_params(labelsize=10)

    os.makedirs(os.path.dirname(PATH_PRICE_CHART), exist_ok=True)
    ax.figure.savefig(PATH_PRICE_CHART, bbox_inches="tight")

if __name__ == '__main__':
    main()