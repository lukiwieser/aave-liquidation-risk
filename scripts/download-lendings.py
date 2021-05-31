from argparse import ArgumentParser
import json

def main(args):
    
    output_file = args.output

    results = dict()

    # write out the results of Q1 and Q2 to JSON file
    with open(output_file, 'w') as fp:
        json.dump(results, fp, indent=4)


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-o', '--output',
                        help='Output file path (JSON)',
                        type=str, required=True)
    args = parser.parse_args()

    main(args)