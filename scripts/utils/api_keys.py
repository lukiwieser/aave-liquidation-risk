from dotenv import find_dotenv, dotenv_values

config = dotenv_values(find_dotenv())

ETHERSCAN_API_KEY = config["ETHERSCAN_API_KEY"]
COINAPI_API_KEY = config["COINAPI_API_KEY"]
DEFIPULSE_API_KEY = config["DEFIPULSE_API_KEY"]
