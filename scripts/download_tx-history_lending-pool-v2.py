import json
import os
from urllib import parse

import pandas as pd
import requests

import utils.api_keys as api_keys

ETHERSCAN_URL = 'https://api.etherscan.io/api'
LENDING_POOL_V2_ADDRESS = '0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9'
# Outputs
PATH_TX_HISTORY = "../data/raw/tx-history_lending-pool-v2.csv"


def main():
    currentblock = 0
    counter = 0
    data = []

    while True:
        url = ETHERSCAN_URL + '?' + parse.urlencode({
            'module': 'account',
            'action': 'txlist',
            'address': LENDING_POOL_V2_ADDRESS,
            'sort': 'asc',
            'startblock': currentblock,
            'endblock': 999999999,
            'apikey': api_keys.ETHERSCAN_API_KEY
        })
        r = requests.get(url)
        d = json.loads(r.text)

        for item in d['result']:
            data.append([item['timeStamp'], item['blockNumber'], item['hash'], item['from'], item['to'], item['input'],
                         item['isError'], item['txreceipt_status']])

        counter = counter + 10000
        if len(data) < counter:
            break
        currentblock = data[counter - 1][1]

        print('Next Block ' + currentblock)

    df = pd.DataFrame(data, columns=['timestamp', 'blockNumber', 'hash', 'from', 'to', 'input', 'isError',
                                     'txreceipt_status'])

    os.makedirs(os.path.dirname(PATH_TX_HISTORY), exist_ok=True)
    df.to_csv(PATH_TX_HISTORY, index=False, header=True)


if __name__ == '__main__':
    main()
