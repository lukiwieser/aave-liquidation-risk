from argparse import ArgumentParser
import json
import urllib.request
from web3_input_decoder import decode_constructor, decode_function

def load_aave_abi(input_file):
    with open(input_file) as json_file:
        aave_abi = json.load(json_file)
        return aave_abi

def main(args):
    input_file = args.input
    output_file = args.output

    aave_abi = load_aave_abi(input_file)
    d = decode_function(
        aave_abi, "0xe8eda9df0000000000000000000000007fc66500c84a76ad7e9c93437bfc5ac33e2ddae9000000000000000000000000000000000000000000000000016345785d8a0000000000000000000000000000dad4c11e8cc6a5c37808d3b31b3b284809f702d10000000000000000000000000000000000000000000000000000000000000000",
    )   
    print(d)

      
if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-o', '--output',
                        help='Output file path (JSON)',
                        type=str, required=False)
    parser.add_argument('-i', '--input',
                        help='Input file path (JSON)', type=str,
                        required=True)
    args = parser.parse_args()

    main(args)