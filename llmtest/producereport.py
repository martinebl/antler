#!/usr/bin/env python3
import sys

from llmtest.filehandler import Filehandler
from llmtest.evaluator import Evaluator
from llmtest.jsonparser import JSONParser

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <file_path> <new_file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    json_data = Filehandler.read_json_file(file_path)
    if json_data is not None:
        attempts = JSONParser.parse_json_as_attempts(json_data["attempts"])
        eval = Evaluator().evaluate(attempts)
        Filehandler.save_to_file(sys.argv[2], str(eval))