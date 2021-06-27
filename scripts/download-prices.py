import pandas as pd
import json
import requests
from urllib import parse
from pathlib import Path


BASE_URL = "https://rest.coinapi.io/v1"
API_KEY = "A098ECCE-FC1E-4594-9C68-9ADF339D40AD"

# saves a pandas dataframe as csv, creates directory if not existent
def save_dataframe(df, out_directory, out_file):
    out_directory = Path(out_directory)
    out_directory.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_directory / out_file, index = False, header=True)


def main():
    assets = [
        "ETH",      #Ethereum
        "DAI", 	    #DAI
        "GUSD",     #Gemini Dollar (GUSD)
        "USDC",     #USD Coin (USDC)
        "USDT",     #USDT Coin (USDT)
        "WETH",     #Wrapped ETH (WETH)
        "BUSD",     #Binance USD (BUSD)
        "SUSD",     #sUSD
        "TUSD",     #TrueUSD (TUSD)
        "AAVE",     #Aave (AAVE)
        "BAT",      #Basic Attention Token (BAT)
        "BAL",      #Balancer (BAL)
        "CRV",      #Curve DAO Token (CRV)
        "ENJ",      #EnjinCoin (ENJ)
        "KNC",      #Kyber Network (KNC)
        "LINK",     #ChainLink (LINK)
        "MANA",     #Decentraland (MANA)
        "MKR",      #Maker (MKR)
        "REN",      #REN
        "SNX",      #SNX
        "UNI",      #Uniswap (UNI)
        "SUSHI",    #xSUSHI (XSUSHI) ?? 			
        "YFI",      #yearn.finance (YFI)
        "ZRX",      #0x Coin (ZRX)
        "RAI"       #RAI
    ]
    quote = "USD"
    queryParams = parse.urlencode({
        'period_id' : '1DAY',
        'time_start' : '2020-12-01T00:00:00',       # 01 Dec 2020 is start of AAVE V2 protocol 
        'limit' : '200',                            # 200 equals 2 requests
        'apikey' : API_KEY
    })

    for i, asset in enumerate(assets):
        url = BASE_URL + "/ohlcv/" + asset + "/" + quote + "/history?" + queryParams
        r = requests.get(url)
        d = json.loads(r.text)

        data = []
        for item in d:
            data.append([item["time_period_start"],item["price_open"], item["price_high"], item["price_low"], item["price_close"]])
        df = pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close'])

        save_dataframe(df, "../data/raw/price-history", asset + "-" + quote + ".csv")

        print(str(i+1) + "/" + str(len(assets)))
    
if __name__ == '__main__':
    main()