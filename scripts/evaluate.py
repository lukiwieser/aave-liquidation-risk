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

    tx_history = load_tx_history(txhistory_file)
    print(str(len(tx_history)))

    for index, row in tx_history.iterrows():
        input_decoded = json.loads(row['input_decoded'])
        print(input_decoded["method"])

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-o', '--output',help='Output file path (JSON)', type=str, required=False)
    parser.add_argument('-t', '--txhistory',help='Input file path of parsed aave tx history (CSV)', type=str,required=True)
    args = parser.parse_args()

    main(args)