#!/usr/bin/env python3
import sys
import random

from llmtest.evaluation import Evaluation
from llmtest.evaluator import Evaluator
from llmtest.jsonparser import JSONParser
from llmtest.filehandler import Filehandler

def calculate_scores_for_length(attempts):
    eval = Evaluator().evaluate(attempts)
    transform_dict = dict()
    # Batches all results for same length transforms into a dictionary where the length of the transform is the key.
    for transform_result in eval.transform_results_original:
        if not transform_result: continue
        length = len(Evaluation.transformResultNameToArray(transform_result.name))
        Evaluator.addToDict(transform_dict, str(length), transform_result.score, transform_result.hit_count, transform_result.all_count)

    # creates rows with all computed averages for each length
    all_averages = [["Length", "Total avg", "Top 10 avg"]]
    for _, (k, v) in enumerate(transform_dict.items()):
        total_avg = sum(float(num[0]) for num in v) / len(v)

        reverse_sorted = sorted(v, reverse=True, key= lambda x: float(x[0]))
        greatest_10 = reverse_sorted[:10]
        top_10_avg = sum(float(num[0]) for num in greatest_10) / len(greatest_10)
        
        all_averages.append([k, total_avg, top_10_avg])

    return all_averages

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file_path> <output_file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    json_data = Filehandler.read_json_file(file_path)
    if json_data is not None:
        attempts = JSONParser.parse_json_as_attempts(json_data["attempts"])

        length_scores = calculate_scores_for_length(attempts)
        Filehandler.write_to_csv(sys.argv[2], length_scores)