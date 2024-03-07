#!/usr/bin/env python3
from llmtest.result import Result

class Evaluation:
    def __init__(self, technique_results: list[Result], transform_results: list[Result], probe_results: list[Result]):
        self.technique_results = technique_results
        self.transform_results = transform_results
        self.probe_results = probe_results

    # def __str__(self) -> str:
    #     output = "\n--- RESULTS ---"
    #     output += "\nClean payloads hit: %i" % len(self.clean_hit_payloads)
        
    #     for i, clean_payload in enumerate(self.clean_hit_payloads):
    #         output += "\nPayload %i: '%s'" % (i+1, clean_payload)

    #     if not self.exploit_scores.items(): 
    #         output += "\nALL PROMPTS HIT CLEAN \nNO EXPLOITS TESTED"
    #     else:
    #         for exploit, score_list in self.exploit_scores.items():
    #             output += "\nExploit: %s - score: %f " % (exploit, sum(score_list) / len(score_list))
    #     return output
        
    def __str__(self) -> str:
        output = "\n--- REPORT ---"

        output += "\n Technique Attack Success Rate (ASR)"
        for res in self.technique_results:
            output += f"\n - {res.getName()}: {res.getScore()*100}% ASR"

        output += "\n Transform Attack Success Rate (ASR)"
        for res in self.transform_results:
            output += f"\n - {res.getName()}: {res.getScore()*100}% ASR"
        
        output += "\n Probe Attack Success Rate (ASR)"
        for res in self.probe_results:
            output += f"\n - {res.getName()}: {res.getScore()*100}% ASR"

        return output