import argparse
import os
import json
from processLines import linesMethod
from straightness import calculate_straightness_rating, calculate_oscillation_rating

def lines(directory):
    linesMethod(directory)

def process_json(json_file, rating_function):
    ratings = rating_function(json_file)
    
    highest_successful_rating = {'file_name': None, 'rating': -float('inf')}
    for rating in ratings:
        print(f"File: {rating['file_name']}, Rating: {rating['rating']} {rating['success']}")
        if rating['success'].strip() == "(successful)" and rating['rating'] > highest_successful_rating['rating']:
            highest_successful_rating = rating
    if highest_successful_rating['file_name']:
        print(f"\nHighest rated successful file: {highest_successful_rating['file_name']}, Rating: {highest_successful_rating['rating']}")

def process_straight_and_oscillate(json_file):
    straight_ratings = calculate_straightness_rating(json_file)
    oscillate_ratings = calculate_oscillation_rating(json_file)
    
    highest_successful_straight = {'file_name': None, 'rating': -float('inf')}
    highest_successful_oscillate = {'file_name': None, 'rating': -float('inf')}
    
    # Find highest rated successful straightness
    for rating in straight_ratings:
        if rating['success'].strip() == "(successful)" and rating['rating'] > highest_successful_straight['rating']:
            highest_successful_straight = rating
    
    # Find highest rated successful oscillation
    for rating in oscillate_ratings:
        if rating['success'].strip() == "(successful)" and rating['rating'] > highest_successful_oscillate['rating']:
            highest_successful_oscillate = rating
    
    # Print the highest ratings found
    if highest_successful_straight['file_name']:
        print(f"Highest rated successful straightness file: {highest_successful_straight['file_name']}, Rating: {highest_successful_straight['rating']}")
        open_lines_image(highest_successful_straight['file_name'], json_file)

    if highest_successful_oscillate['file_name']:
        print(f"Highest rated successful oscillation file: {highest_successful_oscillate['file_name']}, Rating: {highest_successful_oscillate['rating']}")
        open_lines_image(highest_successful_oscillate['file_name'], json_file)

def open_lines_image(file_name, json_file):
    # Assuming 'figures' directory is where the images are saved
    json_folder = os.path.splitext(os.path.basename(json_file))[0].rstrip('_data')
    lines_image_path = f"./rosbags/figures/{json_folder}/{os.path.splitext(file_name)[0]}.png"
    if os.path.exists(lines_image_path):
        os.system(f"start {lines_image_path}") 
    else:
        print(f"Lines image for {file_name} not found.")
def main():
    parser = argparse.ArgumentParser(description='Process a directory and a JSON file.')
    
    # Add a subparser for the commands
    subparsers = parser.add_subparsers(dest='command', help='sub-command help')
    
    # Sub-parser for 'lines' command
    parser_lines = subparsers.add_parser('lines', help='process directory')
    parser_lines.add_argument('directory', metavar='DIR', type=str,
                              help='the directory to process')
    
    # Sub-parser for 'straight' command
    parser_straight = subparsers.add_parser('straight', help='process JSON file for straightness rating')
    parser_straight.add_argument('json_file', metavar='JSON_FILE', type=str,
                                 help='the JSON file to process')

    # Sub-parser for 'oscillate' command
    parser_oscillate = subparsers.add_parser('oscillate', help='process JSON file for oscillation rating')
    parser_oscillate.add_argument('json_file', metavar='JSON_FILE', type=str,
                                  help='the JSON file to process')

    both_oscillate = subparsers.add_parser('both', help='process JSON file for oscillation rating')
    both_oscillate.add_argument('json_file', metavar='JSON_FILE', type=str,
                                  help='the JSON file to process')

    args = parser.parse_args()

    if args.command == 'lines':
        lines(args.directory)

    elif args.command == 'straight':
        process_json(args.json_file, calculate_straightness_rating)

    elif args.command == 'oscillate':
        process_json(args.json_file, calculate_oscillation_rating)
    elif args.command == 'both':
        process_straight_and_oscillate(args.json_file)

if __name__ == '__main__':
    main()
