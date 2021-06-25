from urllib.parse import quote
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
from argparse import ArgumentParser
import codecs
import requests
from urllib import parse
from pathlib import Path

#def main(args):
#    output_file = args.output#
#
#    url = "https://coinmarketcap.com/de/currencies/ethereum/historical-data"
#
#
#    cmc = requests.get(url)
#    soup = BeautifulSoup(cmc.content, 'html.parser')
#    print(soup.title)
#    html = soup.prettify()
#
#    file = codecs.open("lol", "w", "utf-8")
#    file.write(html)
#    file.close()

BASE_URL = "https://rest.coinapi.io/v1"
API_KEY = "A098ECCE-FC1E-4594-9C68-9ADF339D40AD"

# saves a pandas dataframe as csv, creates directory if not existent
def save_dataframe(df, out_directory, out_file):
    out_directory = Path(out_directory)
    out_directory.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_directory / out_file, index = False, header=True)

def main(args):
    output_file = args.output#
    #https://rest.coinapi.io/v1/ohlcv/BTC/USD/history?period_id=1DAY&time_start=2020-12-01T00:00:00&apikey=A098ECCE-FC1E-4594-9C68-9ADF339D40AD&limit=200

    asset = "BTC"
    quote = "USD"
    queryParams = parse.urlencode({
        'period_id' : '1DAY',
        'time_start' : '2020-12-01T00:00:00',       # 01 Dec 2020 is start of AAVE V2 protocol 
        'limit' : '200',                            # 200 equals 2 requests
        'apikey' : API_KEY
    })

    url = BASE_URL + "/ohlcv/" + asset + "/" + quote + "/history?" + queryParams
    r = requests.get(url)
    d = json.loads(r.text)

    data = []
    for item in d:
        data.append([item["time_period_start"],item["price_open"], item["price_high"], item["price_low"], item["price_close"]])
    df = pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close'])

    save_dataframe(df, "../data/raw/price-history", asset + "-" + quote + ".csv")
    #df.to_csv("../data/raw/price-history-" + asset +".csv", index = False, header=True)

    
if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-o', '--output',
                        help='Output file path (JSON)',
                        type=str, required=False)
    args = parser.parse_args()

    main(args)