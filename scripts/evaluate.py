import json
import os
from collections import defaultdict

import pandas as pd

from utils.asset_addresses_and_groups import ASSET_ADDRESSES, ASSET_GROUPS
from utils.classes.Collateral import Collateral
from utils.classes.Loan import Loan
from utils.classes.UserData import UserData
from utils.utils import timestamp_to_simple_iso, hexunit256_to_int, strip_0x_from_address, sort_dict_by_value, \
    round_dict_values

# Inputs
PATH_TX_HISTORY_LENDING_POOL_V2 = "../data/parsed/tx-history_lending-pool-v2.csv"
PATH_TX_HISTORY_WETH_GATEWAY = "../data/parsed/tx-history_weth-gateway.csv"
# Outputs
PATH_RESULTS_SUMMARY = "../results/data/summary.json"
PATH_LIQUIDATION_TIMELINE = "../results/data/liquidation_timeline.csv"

LENDING_POOL_V2_ADDRESS = "7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9"


def main():
    results = dict()

    tx_history = pd.read_csv(PATH_TX_HISTORY_LENDING_POOL_V2, sep=";")
    tx_history_weth_gateway = pd.read_csv(PATH_TX_HISTORY_WETH_GATEWAY, sep=";")

    tx_method_types = defaultdict(int)
    liqidation_addresses_debt = defaultdict(int)
    liqidation_addresses_collateral = defaultdict(int)
    liqidation_addresses_pair = defaultdict(int)
    user_data = dict()
    liquidation_timeline = []

    for index, row in tx_history.iterrows():
        input_decoded = json.loads(row['input_decoded'])

        # count method types:
        if row["isError"] == 0:
            tx_method_types[input_decoded["method"]] += 1

        # collect all dept & collateral addresses
        if input_decoded["method"] == "liquidationCall" and row["isError"] == 0:
            collateralAssetAddress = input_decoded["inputs"][0]
            debtAssetAddress = input_decoded["inputs"][1]

            collateralAsset = ASSET_ADDRESSES[collateralAssetAddress]
            debtAsset = ASSET_ADDRESSES[debtAssetAddress]
            pair = collateralAsset + "/" + debtAsset

            liqidation_addresses_collateral[collateralAsset] += 1
            liqidation_addresses_debt[debtAsset] += 1
            liqidation_addresses_pair[pair] += 1

            timestamp = row["timestamp"]
            date = timestamp_to_simple_iso(timestamp, True)
            collateral_asset_grouped = ASSET_GROUPS.get(collateralAsset, collateralAsset)
            debt_asset_grouped = ASSET_GROUPS.get(debtAsset, debtAsset)
            pair_grouped = collateral_asset_grouped + "/" + debt_asset_grouped
            liquidation_timeline.append([date, pair_grouped])

        # make debt_timeline (excluding ETH)
        if input_decoded["method"] == "borrow" and row["isError"] == 0:
            asset_address = input_decoded["inputs"][0]
            asset = ASSET_ADDRESSES.get(asset_address, asset_address)

            amount = hexunit256_to_int(input_decoded["inputs"][1])
            timestamp = row["timestamp"]
            user = strip_0x_from_address(input_decoded["inputs"][4])  # onBehalfOf
            if user not in user_data:
                user_data[user] = UserData()
            user_data[user].add_borrow(asset, amount, timestamp)

        if input_decoded["method"] == "repay" and row["isError"] == 0:
            asset_address = input_decoded["inputs"][0]
            asset = ASSET_ADDRESSES.get(asset_address, asset_address)
            amount = hexunit256_to_int(input_decoded["inputs"][1])
            timestamp = row["timestamp"]
            user = strip_0x_from_address(input_decoded["inputs"][3])  # onBehalfOf
            if user not in user_data:
                user_data[user] = UserData()
            user_data[user].add_repay(asset, amount, timestamp)

        if input_decoded["method"] == "liquidationCall" and row["isError"] == 0:
            debt_asset_address = input_decoded["inputs"][1]
            debt_asset = ASSET_ADDRESSES.get(debt_asset_address, debt_asset_address)
            debt_to_cover = hexunit256_to_int(input_decoded["inputs"][3])
            timestamp = row["timestamp"]
            user = strip_0x_from_address(input_decoded["inputs"][2])
            if user not in user_data:
                user_data[user] = UserData()
            user_data[user].add_liquidation_victim(debt_asset, debt_to_cover, timestamp)

        # make collateral timeline (excluding ETH)
        if input_decoded["method"] == "deposit" and row["isError"] == 0:
            asset_address = input_decoded["inputs"][0]
            asset = ASSET_ADDRESSES.get(asset_address, asset_address)
            amount = hexunit256_to_int(input_decoded["inputs"][1])
            timestamp = row["timestamp"]
            user = strip_0x_from_address(input_decoded["inputs"][2])  # onBehalfOf
            if user not in user_data:
                user_data[user] = UserData()
            user_data[user].add_deposit(asset, amount, timestamp)

        if input_decoded["method"] == "withdraw" and row["isError"] == 0:
            asset_address = input_decoded["inputs"][0]
            asset = ASSET_ADDRESSES.get(asset_address, asset_address)
            amount = hexunit256_to_int(input_decoded["inputs"][1])
            timestamp = row["timestamp"]
            user = strip_0x_from_address(row["from"])
            if user not in user_data:
                user_data[user] = UserData()
            user_data[user].add_withdraw(asset, amount, timestamp)

    weth_gateway_methods = defaultdict(int)

    for index, row in tx_history_weth_gateway.iterrows():
        if row["isError"] == 0:
            input_decoded = json.loads(row['input_decoded'])
            timestamp = row["timestamp"]
            lending_pool_address = input_decoded["inputs"][0]

            if lending_pool_address.lower() == LENDING_POOL_V2_ADDRESS.lower():
                weth_gateway_methods[input_decoded["method"]] += 1
                # collateral timeline
                if input_decoded["method"] == "depositETH":
                    amount = int(row["value"])
                    user = strip_0x_from_address(input_decoded["inputs"][1])
                    if user not in user_data:
                        user_data[user] = UserData()
                    user_data[user].add_deposit("WETH", amount, timestamp)
                if input_decoded["method"] == "withdrawETH":
                    amount = hexunit256_to_int(input_decoded["inputs"][1])
                    user = strip_0x_from_address(row["from"])
                    if user not in user_data:
                        user_data[user] = UserData()
                    user_data[user].add_withdraw("WETH", amount, timestamp)

                # debt timeline
                if input_decoded["method"] == "borrowETH":
                    amount = hexunit256_to_int(input_decoded["inputs"][1])
                    user = strip_0x_from_address(row["from"])
                    if user not in user_data:
                        user_data[user] = UserData()
                    user_data[user].add_borrow("WETH", amount, timestamp)
                if input_decoded["method"] == "repayETH":
                    amount = hexunit256_to_int(input_decoded["inputs"][1])
                    user = strip_0x_from_address(input_decoded["inputs"][3])
                    if user not in user_data:
                        user_data[user] = UserData()
                    user_data[user].add_repay("WETH", amount, timestamp)

    # group liquidated asset pairs
    liquidated_pairs_grouped = defaultdict(int)
    for pair, count in liqidation_addresses_pair.items():
        pair_arr = pair.split("/")
        collateral = pair_arr[0]
        debt = pair_arr[1]
        collateral_new = ASSET_GROUPS.get(collateral, collateral)
        debt_new = ASSET_GROUPS.get(debt, debt)
        pair_new = collateral_new + "/" + debt_new
        liquidated_pairs_grouped[pair_new] += count

    # sort collateral & debt timelines cronologicaly
    for user, data in user_data.items():
        data.sort_timelines()
        user_data[user] = data

    # calc probelmatic/not probelmatic loans from debt-timeline
    loans_with_problems = defaultdict(int)
    loans_with_no_problems = defaultdict(int)
    loans_with_no_problems_open = defaultdict(int)
    collateral_assets_closed = defaultdict(int)
    collateral_assets_open = defaultdict(int)
    pairs_without_problems = defaultdict(int)

    for user, data in user_data.items():

        collateral_intervals = defaultdict(list)
        for asset, events in data.collateral_timeline.items():
            balance = 0
            totalAddedAmount = 0
            currentCollateralStartTimestamp = -1
            for event in events:
                action = event[0]
                amount = event[1]
                timestamp = event[2]
                if action == "deposit":
                    if currentCollateralStartTimestamp == -1:
                        currentCollateralStartTimestamp = timestamp
                    balance += amount
                    totalAddedAmount += amount
                if action == "withdraw":
                    if amount == -1:
                        balance = 0
                    else:
                        balance -= amount
                    # check if collateral is closed
                    if balance <= 0:
                        collateral_intervals[asset].append(
                            Collateral(currentCollateralStartTimestamp, timestamp, totalAddedAmount))
                        balance = 0
                        totalAddedAmount = 0
                        currentCollateralStartTimestamp = -1
            # check if collateral is still open
            if balance > 0:
                collateral_intervals[asset].append(Collateral(currentCollateralStartTimestamp, -1, totalAddedAmount))
        # count
        for asset, collaterals in collateral_intervals.items():
            for collateral in collaterals:
                if collateral.t2 == -1:
                    collateral_assets_open[asset] += 1
                else:
                    collateral_assets_closed[asset] += 1

        # pairs_with_problems = dict()
        for asset, events in data.debt_timeline.items():
            # determine loan
            loans = []
            debt = 0
            currentLoanStartTimestamp = -1
            hasCurrentDebtLiquidations = False
            for event in events:
                action = event[0]
                amount = event[1]
                timestamp = event[2]
                if action == "borrow":
                    if currentLoanStartTimestamp == -1:
                        currentLoanStartTimestamp = timestamp
                    debt += amount
                if action == "repay":
                    if amount == -1:
                        debt = 0
                    else:
                        debt -= amount
                if action == "liquidation":
                    if amount == -1:
                        debt = debt / 2  # we assume 50% are paid, but the exact value doesnt matter
                    else:
                        debt -= amount
                    hasCurrentDebtLiquidations = True
                # check if loan was paid back
                if action == "repay" or action == "liquidation":
                    timestamp = event[2]
                    if debt <= 0:
                        loans.append(Loan(currentLoanStartTimestamp, timestamp, "repayed", hasCurrentDebtLiquidations))
                        debt = 0
                        currentLoanStartTimestamp = -1
                        hasCurrentDebtLiquidations = False
            # check if loan is open
            if debt > 0:
                loans.append(Loan(currentLoanStartTimestamp, -1, "open", hasCurrentDebtLiquidations))
            # count loans
            for loan in loans:
                if loan.hasLiquidation:
                    loans_with_problems[asset] += 1
                else:
                    if loan.status == "repayed":
                        loans_with_no_problems[asset] += 1
                    if loan.status == "open":
                        loans_with_no_problems_open[asset] += 1
                        # pairs:
            for loan in loans:
                pairs = []
                for collateral_asset, collaterals in collateral_intervals.items():
                    for collateral in collaterals:
                        # check if loan is overlapped by a collateral that is not liquidated
                        if (int(loan.t1) >= int(collateral.t1)) and ((int(collateral.t2) == -1) or (
                                int(loan.t2) != -1 and int(loan.t2) <= int(collateral.t2))):
                            pair = collateral_asset + "/" + asset
                            if not loan.hasLiquidation:
                                pairs.append(pair)
                for pair in pairs:
                    weigth = round(1 / len(pairs), 4)
                    pairs_without_problems[pair] += weigth

    # group pairs_without_problems:
    loan_pairs_without_problems_grouped = defaultdict(int)
    for pair, count in pairs_without_problems.items():
        collateral = pair.split("/")[0]
        debt = pair.split("/")[1]
        collateral_new = ASSET_GROUPS.get(collateral, collateral)
        debt_new = ASSET_GROUPS.get(debt, debt)
        pair_new = collateral_new + "/" + debt_new
        loan_pairs_without_problems_grouped[pair_new] += count

    loans_with_no_problems_sum = sum(loans_with_no_problems.values())
    loans_with_problems_sum = sum(loans_with_problems.values())
    loans_with_no_problems_open_sum = sum(loans_with_no_problems_open.values())
    pairs_without_problems_sum = sum(pairs_without_problems.values())
    loan_pairs_without_problems_coverage = pairs_without_problems_sum / (
            loans_with_no_problems_open_sum + loans_with_no_problems_sum)

    collateral_assets_closed_sum = sum(collateral_assets_closed.values())
    collateral_assets_open_sum = sum(collateral_assets_open.values())

    # calc grouped liquidation risk
    liquidation_risk_per_pair_grouped = dict()
    for pair, count in loan_pairs_without_problems_grouped.items():
        liquidations = liquidated_pairs_grouped.get(pair, 0)
        count_scaled = count / loan_pairs_without_problems_coverage
        risk = liquidations / count_scaled
        liquidation_risk_per_pair_grouped[pair] = risk

    loans_all = loans_with_no_problems_sum + loans_with_no_problems_open_sum + loans_with_problems_sum
    risk_of_loan_with_problem = loans_with_problems_sum / (loans_all)

    df_liquidation_timeline = pd.DataFrame(liquidation_timeline, columns=['date', 'pair'])
    df_liquidation_timeline = df_liquidation_timeline.groupby(['date', 'pair']).date.agg('count').to_frame(
        'liquidations').reset_index()
    df_liquidation_timeline = df_liquidation_timeline.sort_values('date')

    tx_count = dict()
    tx_count["lending_pool"] = len(tx_history.index)
    tx_count["weth_gateway"] = len(tx_history_weth_gateway.index)
    tx_count["all"] = tx_count["lending_pool"] + tx_count["weth_gateway"]

    for method_type, count in weth_gateway_methods.items():
        if method_type == "depositETH":
            tx_method_types["deposit"] += count
        elif method_type == "withdrawETH":
            tx_method_types["withdraw"] += count
        elif method_type == "repayETH":
            tx_method_types["repay"] += count
        elif method_type == "borrowETH":
            tx_method_types["borrow"] += count
        else:
            tx_method_types[method_type] = count

    liquidations_per_borrows = tx_method_types.get("liquidationCall", 0) / tx_method_types.get("borrow", 0)

    results["tx_count"] = tx_count
    results['tx_method_types'] = tx_method_types
    results['liquidations_per_borrows'] = liquidations_per_borrows

    results['liquidated_debt_assets'] = sort_dict_by_value(liqidation_addresses_debt, reverse=True)
    results['liquidated_colateral_assets'] = sort_dict_by_value(liqidation_addresses_collateral, reverse=True)

    results['liquidated_pairs (collateral / debt)'] = sort_dict_by_value(liqidation_addresses_pair, reverse=True)
    results['liquidated_pairs_grouped (collateral / debt)'] = sort_dict_by_value(liquidated_pairs_grouped, reverse=True)

    results["loans_without_problems_open_count"] = loans_with_no_problems_open_sum
    results["loans_without_problems_repayed_count"] = loans_with_no_problems_sum
    results["loans_with_problems_count"] = loans_with_problems_sum
    results["risk_of_loan_with_problem"] = risk_of_loan_with_problem
    results["loans_with_problems"] = sort_dict_by_value(loans_with_problems, reverse=True)
    results["loans_with_no_problems"] = sort_dict_by_value(loans_with_no_problems, reverse=True)

    results["loan_pairs_without_problems_coverage"] = round(loan_pairs_without_problems_coverage, 2)
    results["loan_pairs_without_problems_sum"] = round(pairs_without_problems_sum, 0)
    # results["loan_pairs_without_problems"] = sort_dict_by_value(round_dict_values(pairs_without_problems, 0), reverse=True)
    results["loan_pairs_without_problems_grouped"] = sort_dict_by_value(
        round_dict_values(loan_pairs_without_problems_grouped, 0), reverse=True)

    results["liquidation_risk_per_pair_grouped"] = sort_dict_by_value(
        round_dict_values(liquidation_risk_per_pair_grouped, 6), reverse=True)

    results["collateral_assets_open_sum"] = collateral_assets_open_sum
    results["collateral_assets_closed_sum"] = collateral_assets_closed_sum
    results["collateral_assets_open"] = sort_dict_by_value(collateral_assets_open, reverse=True)
    results["collateral_assets_closed"] = sort_dict_by_value(collateral_assets_closed, reverse=True)

    os.makedirs(os.path.dirname(PATH_LIQUIDATION_TIMELINE), exist_ok=True)
    df_liquidation_timeline.to_csv(PATH_LIQUIDATION_TIMELINE, index=False, header=True)

    os.makedirs(os.path.dirname(PATH_RESULTS_SUMMARY), exist_ok=True)
    with open(PATH_RESULTS_SUMMARY, 'w') as fp:
        json.dump(results, fp, indent=4)

    # with open('readme.txt', 'w') as f:
    #    for user, data in user_data.items():
    #        f.write("{"+user+"}" + data.to_json())


if __name__ == '__main__':
    main()
