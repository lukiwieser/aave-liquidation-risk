from argparse import ArgumentParser
from urllib import parse
import json
import requests
import pandas as pd

BASE_URL = 'https://api.etherscan.io/api'
API_KEY = 'S7XRYA2VNPPU4ZWPNWGSJT2G7F33NSTNP7'
ADDRESS = '0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9'

def get_address_actions():
    currentblock = 0
    counter = 0
    data = []

    while True:
        url = BASE_URL + '?' + parse.urlencode({'module' : 'account', 'action' : 'txlist', 'address' : ADDRESS, 'sort' : 'asc', 'startblock' : currentblock, 'endblock' : 999999999, 'apikey' : API_KEY})
        r = requests.get(url)
        d = json.loads(r.text)

        for item in d['result']:
            data.append([item['timeStamp'], item['blockNumber'], item['hash'], item['from'], item['to'], item['input'], item['isError'], item['txreceipt_status']])

        counter = counter + 10000
        if len(data) < counter:
            break
        currentblock = data[counter-1][1]

        print('Next Block ' + currentblock)
        
    df = pd.DataFrame(data, columns=['timestamp', 'blockNumber', 'hash', 'from', 'to', 'input', 'isError', 'txreceipt_status'])
    return df

def main(args):

    output_file = args.output

    df = get_address_actions()

    df.to_csv(output_file, index = False, header = True)
    
if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-o', '--output',
                        help='Output file path (JSON)',
                        type=str, required=False)
    args = parser.parse_args()

    main(args)