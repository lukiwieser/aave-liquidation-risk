from argparse import ArgumentParser
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt
import matplotlib.ticker as ticker
import dateutil.parser as dp

def load_tx_history(file):
    df = pd.read_csv(file, sep=",") 
    return df

def main(args):
    pricehistory_file = args.pricehistory
    pricehistory = load_tx_history(pricehistory_file)

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

    ax.figure.savefig('../reports/price-chart.png', bbox_inches="tight")

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-p', '--pricehistory',help='Input file path of price history (CSV)', type=str,required=True)
    args = parser.parse_args()

    main(args)