# AAVE Liquidation Analysis

This project aims to analyze risks associated with borrowing assets on the [AAVE protocol](https://aave.com).
Due to the protocols nature, there is always a risk of one’s collateral to be liquidated.

This project was created from students as part of a lecture at the [Technical Univeristy of Vienna](https://www.tuwien.at).

## Step by step go through
1. Download the Aave abi using the download-abi.js script
2. Enter your API Key for the Etherscan API into the download-lendings.py script
3. Download the raw lending Data of the Aave: Lending Pool V2 address using the download-lendings.py script 
    - Specify the output path of the file e.g. python download-lendings.py -o "C:\YourPath\ ... \data\raw\tx-history.csv"
4. Decode the Ether-tx inputs in tx-history.csv using the node parse-lendings.js script
5. Use the evaluate.py script to analyse the data
    - Specify -t & -o e.g. python evaluate.py -t "C:\YourPath\ ... \data\parsed\tx-history.csv" -o "C:\YourPath\ ... \output.json"