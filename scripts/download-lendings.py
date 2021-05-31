from argparse import ArgumentParser
from urllib import parse
import json
import requests

BASE_URL = 'https://api.etherscan.io/api'
API_KEY = 'S7XRYA2VNPPU4ZWPNWGSJT2G7F33NSTNP7'
ADDRESS = '0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9'

def get_address_info():
    url = BASE_URL + '?' + parse.urlencode({'module' : 'account', 'action' : 'txlist', 'address' : ADDRESS, 'sort' : 'asc', 'startblock' : 0, 'endblock' : 999999999, 'apikey' : API_KEY})
    r = requests.get(url)
    d = json.loads(r.text)
  
def main(args):

    output_file = args.output

    results = dict()

    # write out the results of Q1 and Q2 to JSON file
    # with open(output_file, 'w') as fp:
    #   json.dump(results, fp, indent=4)
    get_address_info()


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-o', '--output',
                        help='Output file path (JSON)',
                        type=str, required=False)
    args = parser.parse_args()

    main(args)