# AAVE Liquidation Risk

This project aims to analyze risks associated with borrowing cryptocurrencies on the [AAVE V2 protocol](https://aave.com).

AAVE is a leading decentralized finance protocol running on the Ethereum blockchain (as of 2021). 
It is like a digital bank where you can deposit your cryptocurrencies and earn interest,
or borrow different cryptocurrencies.

When borrowing a cryptocurrency, you must first deposit a certain amount of another cryptocurrency as collateral.
Due to price fluctuations of cryptocurrencies, there is a slight risk that this collateral gets liquidated.

## Findings

### Data Gathering

Here is a short overview of the datasets used in this project:
* AAVE Transactions:
  * 235,000 transactions from the smart contracts Lending Pool V2 (`0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9`) and WETH Gateway (`0xcc9a0B7c43DC2a5F023Bb9b738E45B0Ef6B06E04`)
  * Source: Etherscan API
* AAVE ABI:
  * For decoding contract methods
  * Source: npm package @aave/protocol-v2 and Etherscan API
* Price History:
  * For exploring correlation with asset prices
  * Source: Coinapi API
* AAVE TVL History:
  * For general data exploration
  * Source: Defipulse API

### Data Analysis

#### Contract Events

First, let's take a look at the activities happening on AAVE.

The methods that each transaction invokes on the AAVE smart contract are encoded. 
This can be seen by the field `input` below:

![transaction-data.png](docs/transaction-data.png)

Decoding this input with the AAVE V2 ABI, and counting the number of events yields the following result:

| Contract Event  | Count |
|-----------------|------:|
| deposit         | 93695 |
| withdraw        | 47445 |
| borrow          | 62417 |
| repay           | 29392 |
| liquidationCall |   249 |

Liquidations only make up a small number of all the interactions.
There are less repays than borrows.
This indicates that users borrow multiple times, and then repay these cryptocurrencies in one transaction.
To get more information about borrows & repays, we have to look at individual loans.

#### Loans

Next lets look at individual loans.

| Loan            | Count |
|-----------------|------:|
| open            | 11644 |
| closed          | 13565 |
| liquidated      |   159 |

The number of open and closed loans is similar, suggesting a relatively young protocol. The number of liquidated loans is still small. The share of liquidated loans is `0.63%`, allowing a basic estimate for liquidation risk.

#### Loans per Asset Pair

Next, we try to determine if certain asset pairs are more prone to liquidations than others.
An asset pair is composed of the cryptocurrencies as collateral and of the loan e.g. (ETH-USD).

AAVE does not give us this information, thus we use a simple heuristic: 
If a user has an open loan of asset x, we look at what asset y they have during that time as collateral.

Additionally, we grouped all stable coins that represent USD together (e.g. DAI, USDC).

![loans-without-liquidations.](docs/loans-without-liquidations.png)
Here we see the number of loans without liquidations for certain asset pairs.
Most loans are in ETH-USD (collateral-debt). The 4th most popular is USD-USD.

![loans-with-liquidations](docs/loans-with-liquidations.png)
Here we see the share of loans with liquidations. We also call this *asset pair risk*.
Loans with ETH-USD which were the most popular overall, also have one of the highest percentages of loans with liquidations.
While loans with USD-USD, which are also very popular, have a quite low share of being liquidated.
 
A possible reason could be that loans that involve two stable coins like USD-USD are less prone to liquidations due to less changes in prices.

#### Correlation of liquidations and asset price

Next, lets look if liquidations correlate when the price of a cryptocurrency changes.
Due to time constrains, we just look at the price of ETH.

![correlation-liquidations-and-price](docs/correlation-liquidations-and-price.png)

The price of ETH is shown in the upper chart, while a scatterplot of the liquidations is shown below.
There seems to be a large clusters of liquidations occurring when the price drops are strong, indicating a correlation.

### Summary

Liquidations make up a relatively small number of all interactions on the AAVE V2 protocol.
We determined about 25k loans on the protocol, of which half was paid back, and the other half still open.

Some asset pairs (collateral-dept) are more popular than others, and some are more risky than others.

There seems to be a correlation of liquidations and the price of cryptocurrencies, especially when the price drops stringly.

## Reproduce

To reproduce our results, follow these steps:

1. **Install Dependencies**:

   Ensure that [Node](https://nodejs.org/en/) and [Python 3](https://www.python.org/downloads/) are installed on your machine.

   Install the JavaScript dependencies with:
   ```bash
   npm install
   ```
   Install the Python dependencies with:
   ```bash
   pip install -r requirements.txt
   ```
   *Note:* We additionally use Node, since it is easier to handle ABI related things with the libraries available in the node ecosystem.

2. **Set API Keys:**

   Get API keys from the following sources:
   - [Etherscan](https://docs.etherscan.io/getting-started/viewing-api-usage-statistics)
   - [Defipulse](https://data.defipulse.com)
   - [CoinAPI](https://docs.coinapi.io)
   
   Next, create a `.env` file at the project's root.
   The content of the file should look like `.env.sample` but with your API keys instead of the `xxxx`.

3. **Run the Scripts:**

   The code in the `/scripts` folder follows a pipeline with 4 phases:
   1. Download: Fetch necessary raw data.
   2. Parse: Speeds up processing by parsing some of the raw data.
   3. Evaluate: Analyzes data, generating project results (= heart of the project).
   4. Visualize: Creates plots based on result data.
   
   Simply run the scripts sequentially, starting with "download" scripts.
   Use commands like `node ./scripts/parse-lendings.js`, or `python ./scripts/evaluate.py`. 
   Some scripts might want you to specify the path to the input data.

4. **View Outputs:**

   The results from the scripts will be saved in the following folders:
   - `data/raw`: Contains raw downloaded data.
   - `data/parsed`: Contains the parsed data.
   - `reports`: Contains the final results.


## Credits

This project was created by two students as part of a lecture at the *Vienna University of Technology*.
