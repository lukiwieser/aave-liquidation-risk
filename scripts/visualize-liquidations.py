from argparse import ArgumentParser
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt
import matplotlib.ticker as ticker

def load_tx_history(file):
    df = pd.read_csv(file, sep=";") 
    return df

def main(args):
    txhistory_file = args.txhistory
    tx_history = load_tx_history(txhistory_file)

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

    ax.figure.savefig('../reports/liquidation-chart.png', bbox_inches="tight")

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-t', '--txhistory',help='Input file path of parsed aave tx history (CSV)', type=str,required=True)
    args = parser.parse_args()

    main(args)