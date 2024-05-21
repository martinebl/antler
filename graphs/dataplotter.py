#!/usr/bin/env python3
import sys
import pandas as pd
import matplotlib.pyplot as plt

def handle_data(df, model_name):
    df.plot(marker='o', linestyle='-')
    plt.xticks(range(1, len(df.index)+1), df.index)
    plt.ylabel("Average ASR [0-1]")
    plt.xlabel("Length of transform")
    plt.title("Transform lengths: " + model_name)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <file_path> <model_name>")
        sys.exit(1)
        
    
    file_path = sys.argv[1]
    df = pd.read_csv(file_path, index_col=0)
    if df is not None:
        handle_data(df, sys.argv[2])