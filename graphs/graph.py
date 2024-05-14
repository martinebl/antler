#!/usr/bin/env python3
import sys
import statistics
import pandas as pd
import matplotlib.pyplot as plt

from llmtest.jsonparser import JSONParser
from llmtest.filehandler import Filehandler
from llmtest.attempt import Attempt

def createScorings(attempts: list[Attempt]):
    scorings: list[tuple[str, float]] = []

    current_scoring_probes = []
    current_transform: str = ""
    current_score_sum: float = 0
    for i, attempt in enumerate(attempts):
        current_scoring_probes.append(attempt.getProbe())
        current_transform = attempt.getTransform()
        current_score_sum += attempt.getAttemptSuccessRate()

        if i+1 >= len(attempts) or attempts[i+1].getProbe() in current_scoring_probes:
            # appends current scoring
            scorings.append((current_transform, current_score_sum/len(current_scoring_probes)))
            # resets for new scoring
            current_scoring_probes = []
            current_transform = ""
            current_score_sum = 0

    return scorings

def createData(scorings: list[tuple[str, float]]) -> float:
    data = [["iteration", "max_value", "top_quartile", "median_value", "bot_quartile", "min_value"]]

    for i in range(len(scorings)):
        sub_scorings = [scoring[1] for scoring in scorings[:i+1]]
        sorted_sub_scorings = sorted(sub_scorings)
        max_value = max(sub_scorings)
        min_value = min(sub_scorings)

        median_value = statistics.median(sorted_sub_scorings)
        bot_quartile = statistics.median(sorted_sub_scorings[:len(sorted_sub_scorings)//2]) if len(sub_scorings) > 1 else sub_scorings[0]
        top_quartile = statistics.median(sorted_sub_scorings[len(sorted_sub_scorings)//2:]) if len(sub_scorings) > 1 else sub_scorings[0]

        data.append([i, max_value, top_quartile, median_value, bot_quartile, min_value])

    return data

def plot_graph(data, name):
    df = pd.DataFrame(data[1:], columns=data[0])
    df.set_index("iteration", inplace=True)
    df.plot()
    # Customize y-axis ticks
    plt.yticks([i/10 for i in range(11)])
    # Set y-axis limit
    plt.ylim(0, 1)
    plt.ylabel("ASR [0-1]")
    plt.title(name.split("\\")[-1].split("/")[-1])

    path = '.'.join(name.split(".")[:-1])
    plt.savefig(path + ".png")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    json_data = Filehandler.read_json_file(file_path)
    if json_data is not None:
        attempts = JSONParser.parse_json_as_attempts(json_data["attempts"])
        scorings = createScorings(attempts)
        data = createData(scorings)
        plot_graph(data, sys.argv[1])