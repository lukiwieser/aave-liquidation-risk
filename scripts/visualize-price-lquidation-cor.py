import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt
import matplotlib.ticker as ticker
import dateutil.parser as dp



def main():
    df_prices_eth_usd = pd.read_csv("../data/raw/price-history/ETH-USD.csv") 
    df_liquidation_timeline = pd.read_csv("../reports/liquidation_timeline.csv") 
    pair = "ETH/USD"

    #days_to_consider = 1
    #factor = 0.2
    price_deltas_arr = []
    for index, row in df_prices_eth_usd.iterrows():
        date = row["date"]
        price_delta = (row["high"] - row["low"])/row["high"]
        #price_delta_sum = price_delta
        #for x in range(1,days_to_consider-1):
        #    price_delta_sum += price_deltas_arr[-x][1] * pow(factor,x) if len(price_deltas_arr) >= x else price_delta
        #price_delta_avg = price_delta_sum / days_to_consider

        price_deltas_arr.append([date,price_delta])

    #for item in price_deltas_arr:
    #    date = item[0]
    #    price_delta = item[1]
    #    price_deltas_dict[date] = price_delta

    days_to_consider = 2
    price_deltas_dict = dict()
    for i in range(0, len(price_deltas_arr)):
        date = price_deltas_arr[i][0]

        price_delta_sum = 0
        for x in range(0, days_to_consider):
            price_delta_sum += price_deltas_arr[i-x][1] if i >= x else price_deltas_arr[0][1]
        price_delta_avg = price_delta_sum / days_to_consider
        price_deltas_dict[date] = price_delta_avg


    data = []
    for index, row in df_liquidation_timeline.iterrows():
        if pair == row["pair"]:
            date = row["date"]
            liquidations_count = row["liquidations"]
            price_delta = price_deltas_dict[date]
            data.append([liquidations_count, price_delta, date])
    df = pd.DataFrame(data, columns=['liquidations_count', 'price_delta', 'date'])

    sns.set_theme()
    ax = sns.relplot(data=df, x="liquidations_count", y="price_delta", hue="date")
    ax.set(ylim=(0, None))
    ax.savefig('../reports/price-corr.png', bbox_inches="tight")


if __name__ == '__main__':
    main()