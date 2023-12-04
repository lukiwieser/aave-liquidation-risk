import json
import os
from argparse import ArgumentParser
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt
import matplotlib.ticker as ticker
import dateutil.parser as dp

# Inputs
PATH_RESULTS_SUMMARY = "../data/results/summary.json"
# Outputs
PATH_PLOT_TOP_PAIRS = "../results/plots/asset-top-pairs.png"

def main():
    # read in data
    with open(PATH_RESULTS_SUMMARY) as f:
        results_summary = json.load(f)
    loan_pairs_without_problems_grouped = pd.DataFrame.from_dict(results_summary["loan_pairs_without_problems_grouped"], orient='index').reset_index()
    loan_pairs_without_problems_grouped.columns = ["pair", "count"]

    # adjust values for plotting
    loan_pairs_without_problems_grouped["pair"] = loan_pairs_without_problems_grouped["pair"].str.replace("/", "-")

    # only keep the first 22 rows, group all other rows together into `others`
    top_pairs = loan_pairs_without_problems_grouped.head(22).copy()
    bottom_pairs = loan_pairs_without_problems_grouped.tail(-22)
    others_count = bottom_pairs["count"].sum()
    top_pairs.loc[len(top_pairs)] = ['OTHERS',others_count]

    # plot
    fig_dims = (10, 4)
    fig, ax = plt.subplots(figsize=fig_dims)
    sns.set_theme(style="whitegrid")
    ax = sns.barplot(x="pair", y="count", data=top_pairs, ax=ax).set_title('loans without liquidations')
    ax = plt.gca()
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.tick_params(labelsize=10)

    # save plot
    os.makedirs(os.path.dirname(PATH_PLOT_TOP_PAIRS), exist_ok=True)
    ax.figure.savefig(PATH_PLOT_TOP_PAIRS, bbox_inches="tight")

def main2():
    liquidation_risk_pair_grouped = pd.read_csv("../data/top_pairs.csv", sep=",") 
    #AVG = 0.006267

    data = []
    for index, row in liquidation_risk_pair_grouped.iterrows():
        pair = row["pair"].replace("/","-")
        count = row["count"]
        data.append([pair, count])
    df = pd.DataFrame(data, columns=['pair', 'count'])

    fig_dims = (10, 4)
    fig, ax = plt.subplots(figsize=fig_dims)

    sns.set_theme(style="whitegrid")
    ax = sns.barplot(x="pair", y="count", data=df, ax=ax).set_title('loans without liquidations')
    ax = plt.gca()
    #ax.axhline(AVG*100)
    #ax.set_xlabel('asset-pair (collateral/debt)') 
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.tick_params(labelsize=10)

    ax.figure.savefig('../reports/top-pairs.png', bbox_inches="tight")

if __name__ == '__main__':
    main()