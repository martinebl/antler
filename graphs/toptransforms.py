#!/usr/bin/env python3
import sys
from antler.jsonparser import JSONParser
from antler.filehandler import Filehandler
from antler.attempt import Attempt

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

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    json_data = Filehandler.read_json_file(file_path)
    if json_data is not None:
        attempts = JSONParser.parse_json_as_attempts(json_data["attempts"])
        scorings = createScorings(attempts)
        
        filtered_scorings = list(filter(lambda x: x[1] >= 0.5, scorings))
        for score in sorted(filtered_scorings, key= lambda x: x[1], reverse=True)[:25]:
            print(f'{score[1]} - {score[0]}')