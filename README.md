# AAVE Liquidation Risk

This project aims to analyze risks associated with borrowing assets on the [AAVE protocol](https://aave.com).
Due to the protocols nature, there is always a risk of one’s collateral to be liquidated.

This project was created from students as part of a lecture at the [Technical Univeristy of Vienna](https://www.tuwien.at).

## Installation

This project requires [Node](https://nodejs.org/en/) and [Python 3](https://www.python.org/downloads/) to be installed on your machine.

Install the JavaScript dependencies with:
```
npm install
```

Install the Python dependencies with:
```
pip install -r requirements.txt
```

You also have to create a `.env` file at the root of the project. This file is for defining the API Keys. The content of the file should look like `.env.sample`, but with your API Keys instead of the `xxxx`.

## Usage

Important folders:
- *data/raw*: contains the raw, downloaded data
- *data/parsed*: contains the prased data
- *reports*: contains the final results  

This projectas a pipeline with the following steps:
1. *Download*: This steps download all the require raw data
2. *Parse*: Some of the raw data will be parsed, to speed up the time.
3. *Evaluate*: Evaluates the data and creates results (= heart of the project)
4. *Visualize*: Creates plots of the result data
