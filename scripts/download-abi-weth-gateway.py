from urllib import parse
import json
import requests
import pandas as pd
import utils.globals as globals

BASE_URL = 'https://api.etherscan.io/api'
ADDRESS = '0xcc9a0B7c43DC2a5F023Bb9b738E45B0Ef6B06E04'

def main():

    url = BASE_URL + '?' + parse.urlencode({
        'module' : 'contract', 
        'action' : 'getabi',
        'address' : ADDRESS, 
        'apikey' : globals.ETHERSCAN_API_KEY
    })
    r = requests.get(url)
    d = json.loads(r.text)

    abi = json.loads(d["result"])

    with open("../data/raw/abi-weth-gateway.json", 'w') as fp:
        json.dump(abi, fp, indent=4)


if __name__ == '__main__':
    main()