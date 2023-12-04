import json
import os
from argparse import ArgumentParser
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt
import matplotlib.ticker as ticker
import dateutil.parser as dp
import matplotlib.ticker as mtick

# Inputs
PATH_RESULTS_SUMMARY = "../results/data/summary.json"
# Outputs
PATH_PLOT_ASSET_PAIR_RISK = "../results/plots/asset-pair-risk.png"

def main():
    # read in data
    with open(PATH_RESULTS_SUMMARY) as f:
        results_summary = json.load(f)
    liquidation_risk_per_pair = pd.DataFrame.from_dict(results_summary["liquidation_risk_per_pair_grouped"], orient='index').reset_index()
    liquidation_risk_per_pair.columns = ["pair", "risk"]

    # adjust values for plotting
    liquidation_risk_per_pair = liquidation_risk_per_pair[liquidation_risk_per_pair["risk"] > 0.0] # only keep pairs with risk > 0.0
    liquidation_risk_per_pair["pair"] = liquidation_risk_per_pair["pair"].str.replace("/", "-")
    liquidation_risk_per_pair["risk"] = liquidation_risk_per_pair["risk"] * 100

    # plot
    fig_dims = (10, 4)
    fig, ax = plt.subplots(figsize=fig_dims)
    sns.set_theme(style="whitegrid")
    ax = sns.barplot(x="pair", y="risk", data=liquidation_risk_per_pair, ax=ax).set_title('asset-pair risk')
    ax = plt.gca()
    # ax.axhline(0.00076*100) plot avg
    ax.set_xlabel('asset-pair (collateral/debt)')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.tick_params(labelsize=10)

    # save plot
    os.makedirs(os.path.dirname(PATH_PLOT_ASSET_PAIR_RISK), exist_ok=True)
    ax.figure.savefig(PATH_PLOT_ASSET_PAIR_RISK, bbox_inches="tight")


if __name__ == '__main__':
    main()