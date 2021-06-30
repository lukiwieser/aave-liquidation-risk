from argparse import ArgumentParser
from urllib import parse
import json
import requests
import pandas as pd

BASE_URL = 'https://data-api.defipulse.com/api/v1/'
API_KEY = '7899c5701d536f8525c8ae2122c838216d7386e7f9262e842dd80f043938'    # ATTENTION! Defipulse has limits on it's API so be careful.

def get_historical_tvl():
    url = BASE_URL + "defipulse/api/GetHistory?" +  parse.urlencode({
        'api-key' : API_KEY, 
        'project' : 'aave', 
        'period' : 'all',
    })
    r = requests.get(url)
    d = json.loads(r.text)

    data = []
    for item in d:
        data.append([item["timestamp"],item["tvlUSD"],])

    df = pd.DataFrame(data, columns=['timestamp', 'tvlUSD'])
    return df

def main(args):
    output_file = args.output
    df = get_historical_tvl()

    df.to_csv(output_file, index = False, header=True)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-o', '--output',
                        help='Output file path (JSON)',
                        type=str, required=True)
    args = parser.parse_args()

    main(args)