import json
import urllib.request
from web3_input_decoder import decode_constructor, decode_function

with open('../data/out.txt') as json_file:
    aave_abi = json.load(json_file)
    d = decode_function(
        aave_abi, "0xe8eda9df0000000000000000000000007fc66500c84a76ad7e9c93437bfc5ac33e2ddae9000000000000000000000000000000000000000000000000016345785d8a0000000000000000000000000000dad4c11e8cc6a5c37808d3b31b3b284809f702d10000000000000000000000000000000000000000000000000000000000000000",
    )   
    print(d)