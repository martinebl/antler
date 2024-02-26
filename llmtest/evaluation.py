#!/usr/bin/env python3
class Evaluation:
    def __init__(self, clean_hit_payloads: list[str], exploit_scores: dict[str, list[float]]) -> None:
        self.clean_hit_payloads = clean_hit_payloads
        self.exploit_scores = exploit_scores

    def __str__(self) -> str:
        output = "\n--- RESULTS ---"
        output += "\nClean payloads hit: %i" % len(self.clean_hit_payloads)
        
        for i, clean_payload in enumerate(self.clean_hit_payloads):
            output += "\nPayload %i: '%s'" % (i+1, clean_payload)

        if not self.exploit_scores.items(): 
            output += "\nALL PROMPTS HIT CLEAN \nNO EXPLOITS TESTED"
        else:
            for exploit, score_list in self.exploit_scores.items():
                output += "\nExploit: %s - score: %f " % (exploit, sum(score_list) / len(score_list))
                
            #    output += "\nExploit: %s - ASR %i (%i/%i)" % (exploit, (hits/total*100), hits, total)
        
        return output
