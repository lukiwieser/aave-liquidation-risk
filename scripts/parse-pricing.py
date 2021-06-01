import pandas as pd

with open("../data/raw-handpicked/price-history-eth.txt") as f:
    data = []

    count = 0
    for line in f:
        count += 1

        if count != 1:
            tokens = line.split()

            date = tokens[1].replace(",","") + " " + tokens[0] + " " + tokens[2]

            open = float(tokens[4].replace("$","").replace(",","")) 
            high = float(tokens[4].replace("$","").replace(",","")) 
            low = float(tokens[4].replace("$","").replace(",","")) 
            close = float(tokens[4].replace("$","").replace(",","")) 

            data.append([date,open,high,low,close])

    df = pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close'])
    df.to_csv("../data/parsed/price-history-eth.csv", index = False, header=True)
