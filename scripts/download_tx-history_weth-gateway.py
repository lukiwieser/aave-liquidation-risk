import os
from argparse import ArgumentParser
from urllib import parse
import json
import requests
import pandas as pd
import utils.api_keys as api_keys

ETHERSCAN_URL = 'https://api.etherscan.io/api'
WETH_GATEWAY_ADDRESS = '0xcc9a0B7c43DC2a5F023Bb9b738E45B0Ef6B06E04'
# Outputs
PATH_TX_HISTORY = "../data/raw/tx-history_weth-gateway.csv"


def main():
    currentblock = 0
    counter = 0
    data = []

    while True:
        url = ETHERSCAN_URL + '?' + parse.urlencode({
            'module': 'account',
            'action': 'txlist',
            'address': WETH_GATEWAY_ADDRESS,
            'sort': 'asc',
            'startblock': currentblock,
            'endblock': 999999999,
            'apikey': api_keys.ETHERSCAN_API_KEY
        })
        r = requests.get(url)
        d = json.loads(r.text)

        for item in d['result']:
            data.append([item['timeStamp'], item['blockNumber'], item['hash'], item['from'], item['to'], item['value'],
                         item['input'], item['isError'], item['txreceipt_status']])

        counter = counter + 10000
        if len(data) < counter:
            break
        currentblock = data[counter - 1][1]

        print('Next Block ' + currentblock)

    df = pd.DataFrame(data, columns=['timestamp', 'blockNumber', 'hash', 'from', 'to', 'value', 'input', 'isError',
                                     'txreceipt_status'])

    os.makedirs(os.path.dirname(PATH_TX_HISTORY), exist_ok=True)
    df.to_csv(PATH_TX_HISTORY, index=False, header=True)


if __name__ == '__main__':
    main()
