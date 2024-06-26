#!/usr/bin/env python3
import sys

from antler.evaluation import Evaluation
from antler.evaluator import Evaluator
from antler.jsonparser import JSONParser
from antler.filehandler import Filehandler

def calculate_scores_for_length(attempts):
    eval = Evaluator().evaluate(attempts)
    transform_dict = dict()
    # Batches all results for same length transforms into a dictionary where the length of the transform is the key.
    for transform_result in eval.transform_results_original:
        if not transform_result: continue
        length = len(Evaluation.transformResultNameToArray(transform_result.name))
        Evaluator.addToDict(transform_dict, str(length), transform_result.score, transform_result.hit_count, transform_result.all_count)

    # creates rows with all computed averages for each length
    all_averages = [["Length", "Best score", "Top 10% avg", "Top 10 avg", "Total avg"]]
    for _, (length, scores) in enumerate(transform_dict.items()):
        total_avg = sum(float(num[0]) for num in scores) / len(scores)

        reverse_sorted = sorted(scores, reverse=True, key= lambda x: float(x[0]))
        best_score = reverse_sorted[0][0]
        greatest_10 = reverse_sorted[:10]
        top_10_avg = sum(float(num[0]) for num in greatest_10) / len(greatest_10)
        top_10_percent = reverse_sorted[:round(len(scores) / 10)]
        top_10_percent_avg = sum(float(num[0]) for num in top_10_percent) / len(top_10_percent)

        all_averages.append([length, best_score, top_10_percent_avg, top_10_avg, total_avg ])

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