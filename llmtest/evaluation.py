#!/usr/bin/env python3
class Evaluation:
    def __init__(self, clean_hit_payloads: list[str], technique_scores: dict[str, list[float]]) -> None:
        self.clean_hit_payloads = clean_hit_payloads
        self.technique_scores = technique_scores

    def __str__(self) -> str:
        output = "\n--- RESULTS ---"
        output += "\nClean payloads hit: %i" % len(self.clean_hit_payloads)
        
        for i, clean_payload in enumerate(self.clean_hit_payloads):
            output += "\nPayload %i: '%s'" % (i+1, clean_payload)

        if not self.technique_scores.items(): 
            output += "\nALL PROMPTS HIT CLEAN \nNO TECHNIQUES TESTED"
        else:
            for technique, score_list in self.technique_scores.items():
                output += "\ntechnique: %s - score: %f " % (technique, sum(score_list) / len(score_list))
        return output
