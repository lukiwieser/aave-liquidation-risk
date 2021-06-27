from argparse import ArgumentParser
import json
import pandas as pd

def load_tx_history(file):
    df = pd.read_csv(file, sep=";") 
    return df

def main(args):
    txhistory_file = args.txhistory
    output_file = args.output
    results = dict()

    assetAddresses = {
        'dac17f958d2ee523a2206206994597c13d831ec7' : 'USDT', 
        'ba100000625a3754423978a60c9317c58a424e3d' : 'BAL',  
        'c011a73ee8576fb46f5e1c5751ca3b9fe0af2a6f' : 'SNX',  
        '056fd409e1d7a124bd7017459dfea2f387b6d5cd' : 'GUSD', 
        'd533a949740bb3306d119cc777fa900ba034cd52' : 'CRV',  
        '0000000000085d4780b73119b644ae5ecd22b376' : 'TUSD', 
        '57ab1ec28d129707052df4df418d58a2d46d5f51' : 'SUSD', 
        '1f9840a85d5af5bf1d1762f925bdaddc4201f984' : 'UNI',  
        'c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2' : 'WETH', 
        '0d8775f648430679a709e98d2b0cb6250d2887ef' : 'BAT',  
        '2260fac5e5542a773aa44fbcfedf7c193bc2c599' : 'WBTC', 
        '514910771af9ca656af840dff83e8264ecf986ca' : 'LINK', 
        '7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9' : 'AAVE', 
        '408e41876cccdc0f92210600ef50372656052a38' : 'REN',  
        'f629cbd94d3791c9250152bd8dfbdf380e2a3b9c' : 'ENJ',  
        '6b175474e89094c44da98b954eedeac495271d0f' : 'DAI',  
        'a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48' : 'USDC', 
        '8798249c2e607446efb7ad49ec89dd1865ff4272' : 'SUSHI',
        '4fabb145d64652a948d72533023f6e7a623c7c53' : 'BUSD', 
        'e41d2489571d322189246dafa5ebde1f4699f498' : 'ZRX',  
        '0f5d2fb29fb7d3cfee444a200298f468908cc942' : 'MANA', 
    }

    tx_history = load_tx_history(txhistory_file)

    tx_method_types = dict()
    liqidation_addresses_debt = dict()
    liqidation_addresses_collateral = dict()
    liqidation_addresses_pair = dict()

    # all
    # collateral & dept
    # pairs


    for index, row in tx_history.iterrows():
        input_decoded = json.loads(row['input_decoded'])
    	
        # count method types:
        if input_decoded["method"] in tx_method_types:
            tx_method_types[input_decoded["method"]] += 1
        else:
            tx_method_types[input_decoded["method"]] = 1

        # collect all dept & collateral addresses
        if input_decoded["method"] == "liquidationCall" and row["isError"] == 0:
            collateralAssetAddress = input_decoded["inputs"][0]
            debtAssetAddress = input_decoded["inputs"][1]

            collateralAsset = assetAddresses[collateralAssetAddress]
            debtAsset = assetAddresses[debtAssetAddress]

            if collateralAsset in liqidation_addresses_collateral:
                liqidation_addresses_collateral[collateralAsset] += 1
            else:
                liqidation_addresses_collateral[collateralAsset] = 1

            if debtAsset in liqidation_addresses_debt:
                liqidation_addresses_debt[debtAsset] += 1
            else:
                liqidation_addresses_debt[debtAsset] = 1

            pair = collateralAsset + "/" + debtAsset
            if pair in liqidation_addresses_pair:
                liqidation_addresses_pair[pair] += 1
            else:
                liqidation_addresses_pair[pair] = 1

    liqidation_rate_overall = tx_method_types["liquidationCall"] / tx_method_types["borrow"]

    results['liqidation_rate_overall'] = liqidation_rate_overall
    results['tx_method_types'] = tx_method_types
    results['liqidation_addresses_debt'] = liqidation_addresses_debt
    results['liqidation_addresses_collateral'] = liqidation_addresses_collateral
    results['liqidation_addresses_pair'] = {k: v for k, v in sorted(liqidation_addresses_pair.items(), key=lambda item: item[1], reverse=True)}

    with open(output_file, 'w') as fp:
        json.dump(results, fp, indent=4)

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-o', '--output',help='Output file path (JSON)', type=str, required=False)
    parser.add_argument('-t', '--txhistory',help='Input file path of parsed aave tx history (CSV)', type=str,required=True)
    args = parser.parse_args()

    main(args)

