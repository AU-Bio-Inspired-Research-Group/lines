import argparse
import os
import json
from processLines import linesMethod
from straightness import *

def lines(directory):
    linesMethod(directory)

def process_json(json_file):
    ratings = calculate_straightness_rating(json_file)
    for rating in ratings:
        print(f"File: {rating['file_name']}, Straightness Rating: {rating['straightness_rating']}")

def main():
    parser = argparse.ArgumentParser(description='Process a directory and a JSON file.')
    
    # Add a subparser for the 'lines' command
    subparsers = parser.add_subparsers(dest='command', help='sub-command help')
    
    # Sub-parser for 'lines' command
    parser_lines = subparsers.add_parser('lines', help='process directory')
    parser_lines.add_argument('directory', metavar='DIR', type=str,
                              help='the directory to process')
    
    # Sub-parser for 'straight' command
    parser_straight = subparsers.add_parser('straight', help='process JSON file')
    parser_straight.add_argument('json_file', metavar='JSON_FILE', type=str,
                                 help='the JSON file to process')

    args = parser.parse_args()

    if args.command == 'lines':
        lines(args.directory)

    elif args.command == 'straight':
        process_json(args.json_file)

if __name__ == '__main__':
    main()
