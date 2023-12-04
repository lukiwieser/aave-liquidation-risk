import json
import os

import matplotlib.pylab as plt
import matplotlib.ticker as mtick
import pandas as pd
import seaborn as sns

# Inputs
PATH_RESULTS_SUMMARY = "../results/data/summary.json"
# Outputs
PATH_PLOT_ASSET_PAIR_RISK = "../results/plots/asset-pair-risk.png"


def main():
    # read in data
    with open(PATH_RESULTS_SUMMARY) as f:
        results_summary = json.load(f)
    liquidated_asset_pairs = pd.DataFrame.from_dict(results_summary["liquidation_risk_per_pair_grouped"],
                                                       orient='index').reset_index()
    liquidated_asset_pairs.columns = ["pair", "risk"]

    # adjust values for plotting
    liquidated_asset_pairs = liquidated_asset_pairs[liquidated_asset_pairs["risk"] > 0.0]  # only keep with risk > 0.0
    liquidated_asset_pairs["pair"] = liquidated_asset_pairs["pair"].str.replace("/", "-")
    liquidated_asset_pairs["risk"] = liquidated_asset_pairs["risk"] * 100

    # plot
    sns.set_theme()
    fig_dims = (10, 4)
    fig, ax = plt.subplots(figsize=fig_dims)
    ax = sns.barplot(x="pair", y="risk", data=liquidated_asset_pairs, ax=ax, color='b')
    ax = plt.gca()
    # ax.axhline(0.00076*100) plot avg
    ax.set_title('Share of Liquidated Loans per Asset Pair')
    ax.set_xlabel('Asset Pair (Collateral / Debt)')
    ax.set_ylabel("")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.tick_params(labelsize=10)

    # save plot
    os.makedirs(os.path.dirname(PATH_PLOT_ASSET_PAIR_RISK), exist_ok=True)
    ax.figure.savefig(PATH_PLOT_ASSET_PAIR_RISK, bbox_inches="tight")


if __name__ == '__main__':
    main()
