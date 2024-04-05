#!/usr/bin/env python3
import sys
import json
import random

from llmtest.evaluation import Evaluation
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
    
def calculate_scores_for_length(attempts):
    eval = Evaluator().evaluate(attempts)
    transform_dict = dict()
    # Batches all results for same length transforms into a dictionary where the length of the transform is the key.
    for transform_result in eval.transform_results_original:
        if not transform_result: continue
        length = len(Evaluation.transformResultNameToArray(transform_result.name))
        Evaluator.addToDict(transform_dict, str(length), transform_result.score, transform_result.hit_count, transform_result.all_count)

    avg_scores_transform_length = []
    avg_scores_transform_length_top_ten = []
    avg_scores_trans_length_random_ten = []
    for _, (_, v) in enumerate(transform_dict.items()):
        avg = sum(float(num[0]) for num in v) / len(v)
        avg_scores_transform_length.append(avg)

        reverse_sorted = sorted(v, reverse=True, key= lambda x: float(x[0]))
        greatest_10 = reverse_sorted[:10]
        avg = sum(float(num[0]) for num in greatest_10) / len(greatest_10)
        avg_scores_transform_length_top_ten.append(avg)

        random_10 = random.sample(v, 10)
        avg = sum(float(num[0]) for num in random_10) / len(greatest_10)
        avg_scores_trans_length_random_ten.append(avg)

    print(avg_scores_transform_length)
    print(avg_scores_transform_length_top_ten)
    print(avg_scores_trans_length_random_ten)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    json_data = read_json_file(file_path)
    if json_data is not None:
        attempts = JSONParser.parse_json_as_attempts(json_data["attempts"])

        calculate_scores_for_length(attempts)