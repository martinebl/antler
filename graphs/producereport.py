#!/usr/bin/env python3
import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from antler.filehandler import Filehandler
from antler.evaluation import Evaluation
from antler.evaluator import Evaluator
from antler.jsonparser import JSONParser

def savefig(eval: Evaluation, path: str):
    colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'white', 'orange','purple']
    color_change_indexes = []
    for i in range(len(eval.transform_results_original)-1):
        if i == 0: continue
        if len(eval.transform_results_original[i].getName().split(',')) > len(eval.transform_results_original[i-1].getName().split(',')):
            color_change_indexes.append(i)
    color_change_indexes.append(len(eval.transform_results_original))

    df = pd.DataFrame(data={
        "transform":[res.getName() for res in eval.transform_results_original],
        "ASR": [res.getScore() for res in eval.transform_results_original]
    })

    # Plot the bar graph
    ax = df.plot(kind='bar', x='transform', y='ASR')

    current_color_index = 0
    for i, bar in enumerate(ax.patches):
        if i > color_change_indexes[current_color_index]:
            current_color_index += 1
        bar.set_color(colors[current_color_index])

    legend_elements = [Patch(facecolor=colors[i], label=f"Length {i+1}") for i in range(current_color_index + 1)]

    # Adding legend
    plt.legend(handles=legend_elements)
    

    # Set labels and title
    plt.xlabel('Transforms - sorted by length and combination')
    plt.ylabel('ASR')
    plt.title('ASR by Transform')

    # Show the plot
    plt.xticks([])  # Hides all xticks
    plt.tight_layout()  # Adjust layout to prevent clipping of labels
    plt.savefig(path)

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

        figpath = sys.argv[2].split(".")[0]
        savefig(eval, f'{figpath}.png')