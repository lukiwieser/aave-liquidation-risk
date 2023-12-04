import json
from urllib import parse

import requests

import utils.api_keys as api_keys

ETHERSCAN_URL = 'https://api.etherscan.io/api'
WETH_GATEWAY_ADDRESS = '0xcc9a0B7c43DC2a5F023Bb9b738E45B0Ef6B06E04'
PATH_ABI_WETH_GATEWAY = "../data/raw/abi_weth-gateway.json"


def main():
    url = ETHERSCAN_URL + '?' + parse.urlencode({
        'module': 'contract',
        'action': 'getabi',
        'address': WETH_GATEWAY_ADDRESS,
        'apikey': api_keys.ETHERSCAN_API_KEY
    })
    r = requests.get(url)
    d = json.loads(r.text)

    abi = json.loads(d["result"])

    with open(PATH_ABI_WETH_GATEWAY, 'w') as fp:
        json.dump(abi, fp, indent=4)


if __name__ == '__main__':
    main()
