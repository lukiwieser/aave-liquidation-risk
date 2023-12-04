import json
import os

import matplotlib.pylab as plt
import pandas as pd
import seaborn as sns

# Inputs
PATH_RESULTS_SUMMARY = "../results/data/summary.json"
# Outputs
PATH_PLOT_PAIRS = "../results/plots/asset-pairs.png"
PATH_PLOT_PAIRS_WITH_LIQUIDATIONS = "../results/plots/asset-pairs_with-liquidations.png"
PATH_PLOT_PAIRS_WITHOUT_LIQUIDATIONS = "../results/plots/asset-pairs_without-liquidations.png"


def main():
    # read in data
    with open(PATH_RESULTS_SUMMARY) as f:
        results_summary = json.load(f)

    # get asset-pairs with liquidations
    loan_pairs_with_liquidations_grouped = pd.DataFrame.from_dict(
        results_summary["liquidated_pairs_grouped (collateral / debt)"], orient='index').reset_index()
    loan_pairs_with_liquidations_grouped.columns = ["pair", "count"]

    # get asset-pairs without liquidations
    loan_pairs_without_liquidations_grouped = pd.DataFrame.from_dict(
        results_summary["loan_pairs_without_problems_grouped"], orient='index').reset_index()
    loan_pairs_without_liquidations_grouped.columns = ["pair", "count"]

    # get asset-pairs in total
    loan_pairs_grouped = pd.concat([loan_pairs_with_liquidations_grouped, loan_pairs_without_liquidations_grouped])\
        .groupby(['pair']).sum().reset_index()
    loan_pairs_grouped = loan_pairs_grouped.sort_values(by=['count'], ascending=False)

    # plot
    n_pairs = 22
    plot_first_n_pairs(loan_pairs_grouped, n_pairs, "Loans per Asset-Pair", PATH_PLOT_PAIRS)
    plot_first_n_pairs(loan_pairs_without_liquidations_grouped, n_pairs, "Not Liquidated Loans per Asset-Pair",
                       PATH_PLOT_PAIRS_WITHOUT_LIQUIDATIONS)
    plot_first_n_pairs(loan_pairs_with_liquidations_grouped, n_pairs, "Liquidated Loans per Asset Pair",
                       PATH_PLOT_PAIRS_WITH_LIQUIDATIONS)


def plot_first_n_pairs(df, n_pairs, title, path):
    # adjust values for plotting
    df["pair"] = df["pair"].str.replace("/", "-")

    # only keep the first 22 rows, group all other rows together into `others`
    top_pairs = df.head(n_pairs).copy()
    bottom_pairs = df.tail(-n_pairs)
    others_count = bottom_pairs["count"].sum()
    top_pairs.loc[len(top_pairs)] = ['OTHERS', others_count]

    # plot
    sns.set_theme()
    fig_dims = (10, 4)
    fig, ax = plt.subplots(figsize=fig_dims)
    ax = sns.barplot(x="pair", y="count", data=top_pairs, ax=ax, color='b').set_title(title)
    ax = plt.gca()
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.tick_params(labelsize=10)
    ax.set_xlabel("Asset Pair (Collateral / Debt)")
    ax.set_ylabel("Count")

    # save plot
    os.makedirs(os.path.dirname(path), exist_ok=True)
    ax.figure.savefig(path, bbox_inches="tight")
    plt.clf()


if __name__ == '__main__':
    main()
