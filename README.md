# AAVE Liquidation Risk

This project aims to analyze risks associated with borrowing assets on the [AAVE V2 protocol](https://aave.com).

When borrowing an asset on AAVE, the user must deposit a certain amount of collateral.
However, there is always a slight risk that this collateral gets liquidated.

## Findings

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
