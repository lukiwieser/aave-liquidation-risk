from argparse import ArgumentParser
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt
import matplotlib.ticker as ticker
import dateutil.parser as dp

def main():
    liquidation_risk_pair_grouped = pd.read_csv("../data/liquidation_risk_pair_grouped.csv", sep=",") 
    AVG = 0.006267

    data = []
    for index, row in liquidation_risk_pair_grouped.iterrows():
        pair = row["pair"].replace("/","-")
        risk = row["risk"] * 100
        data.append([pair, risk])
    df = pd.DataFrame(data, columns=['pair', 'risk'])

    fig_dims = (10, 4)
    fig, ax = plt.subplots(figsize=fig_dims)

    sns.set_theme(style="whitegrid")
    ax = sns.barplot(x="pair", y="risk", data=df, ax=ax).set_title('asset-pair risk')
    ax = plt.gca()
    ax.axhline(AVG*100)
    ax.set_xlabel('asset-pair (collateral/debt)') 
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.tick_params(labelsize=10)

    ax.figure.savefig('../reports/asset-pair-risk.png', bbox_inches="tight")

if __name__ == '__main__':
    main()