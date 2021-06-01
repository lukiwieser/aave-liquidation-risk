from argparse import ArgumentParser
import json
import urllib.request
from web3_input_decoder import decode_constructor, decode_function
import pandas as pd
import sys

def load_tx_history(file):
    df = pd.read_csv(file, sep=";") 
    return df

def main(args):
    txhistory_file = args.txhistory
    output_file = args.output
    results = dict()


    tx_history = load_tx_history(txhistory_file)

    tx_method_types = dict()
    for index, row in tx_history.iterrows():
        input_decoded = json.loads(row['input_decoded'])

        if input_decoded["method"] in tx_method_types:
            tx_method_types[input_decoded["method"]] += 1
        else:
            tx_method_types[input_decoded["method"]] = 1

        



    results['tx_method_types'] = tx_method_types

    with open(output_file, 'w') as fp:
        json.dump(results, fp, indent=4)

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-o', '--output',help='Output file path (JSON)', type=str, required=False)
    parser.add_argument('-t', '--txhistory',help='Input file path of parsed aave tx history (CSV)', type=str,required=True)
    args = parser.parse_args()

    main(args)

