import json
import os
from urllib import parse

import pandas as pd
import requests

import utils.api_keys as api_keys

DEPIPULSE_URL = 'https://data-api.defipulse.com/api/v1/'
# Output
PATH_TVL_HISTORY = "../data/raw/tvl-history.csv"


def main():
    url = DEPIPULSE_URL + "defipulse/api/GetHistory?" + parse.urlencode({
        'api-key': api_keys.DEFIPULSE_API_KEY,
        'project': 'aave',
        'period': 'all',
    })
    r = requests.get(url)
    d = json.loads(r.text)

    data = []
    for item in d:
        data.append([item["timestamp"], item["tvlUSD"], ])

    df = pd.DataFrame(data, columns=['timestamp', 'tvlUSD'])

    os.makedirs(os.path.dirname(PATH_TVL_HISTORY), exist_ok=True)
    df.to_csv(PATH_TVL_HISTORY, index=False, header=True)


if __name__ == '__main__':
    main()
