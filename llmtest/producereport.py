#!/usr/bin/env python3
import sys
import json

from llmtest.evaluator import Evaluator
from llmtest.jsonparser import JSONParser

""" Reads the contents of a file and parses it as JSON """
def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Unable to parse JSON from '{file_path}'.")
        return None

def save_to_file(file_path, strings):
    try:
        with open(file_path, "w") as file:
            file.write(strings)
    except PermissionError:
        print(f"Error: Permission denied for file '{file_path}'.")
        return None
    except FileExistsError:
        print(f"Error: The file '{file_path}' already exists")
        return None
    except IsADirectoryError:
        print(f"Error: The specified path is a directory '{file_path}'.")
        return None
    except IOError:
        print(f"IOError: An error occured saving to '{file_path}'.")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <file_path> <new_file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    json_data = read_json_file(file_path)
    if json_data is not None:
        attempts = JSONParser.parse_json_as_attempts(json_data["attempts"])
        eval = Evaluator().evaluate(attempts)
        save_to_file(sys.argv[2], str(eval))