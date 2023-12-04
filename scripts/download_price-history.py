import json
from pathlib import Path
from urllib import parse

import pandas as pd
import requests

import utils.api_keys as api_keys
from scripts.utils.utils import simplify_iso_date

COINAPI_URL = "https://rest.coinapi.io/v1"


def main():
    assets = [
        "ETH",  # Ethereum
        "DAI",  # DAI
        "GUSD",  # Gemini Dollar (GUSD)
        "USDC",  # USD Coin (USDC)
        "USDT",  # USDT Coin (USDT)
        "WETH",  # Wrapped ETH (WETH)
        "BUSD",  # Binance USD (BUSD)
        "SUSD",  # sUSD
        "TUSD",  # TrueUSD (TUSD)
        "AAVE",  # Aave (AAVE)
        "BAT",  # Basic Attention Token (BAT)
        "BAL",  # Balancer (BAL)
        "CRV",  # Curve DAO Token (CRV)
        "ENJ",  # EnjinCoin (ENJ)
        "KNC",  # Kyber Network (KNC)
        "LINK",  # ChainLink (LINK)
        "MANA",  # Decentraland (MANA)
        "MKR",  # Maker (MKR)
        "REN",  # REN
        "SNX",  # SNX
        "UNI",  # Uniswap (UNI)
        "SUSHI",  # xSUSHI (XSUSHI) ??
        "YFI",  # yearn.finance (YFI)
        "ZRX",  # 0x Coin (ZRX)
        "RAI"  # RAI
    ]
    quote = "USD"
    queryParams = parse.urlencode({
        'period_id': '1DAY',
        'time_start': '2020-12-01T00:00:00',  # 01 Dec 2020 is start of AAVE V2 protocol
        'limit': '200',  # 200 equals 2 requests
        'apikey': api_keys.COINAPI_API_KEY
    })

    for i, asset in enumerate(assets):
        url = COINAPI_URL + "/ohlcv/" + asset + "/" + quote + "/history?" + queryParams
        r = requests.get(url)
        d = json.loads(r.text)

        data = []
        for item in d:
            date = simplify_iso_date(item["time_period_start"])
            data.append([date, item["price_open"], item["price_high"], item["price_low"], item["price_close"]])
        df = pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close'])

        folder = Path("../data/raw/price-history")
        filename = asset + "-" + quote + ".csv"
        folder.mkdir(parents=True, exist_ok=True)
        df.to_csv(folder / filename, index=False, header=True)

        print(str(i + 1) + "/" + str(len(assets)))


if __name__ == '__main__':
    main()
