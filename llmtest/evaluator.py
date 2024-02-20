#!/usr/bin/env python3
from llmtest.result import Result
from typing import Tuple, List, Dict
from llmtest.transformers.transformer import Transformer

class Evaluator:
    def __init__(self) -> None:
        self = self

    #Every result = 1 probe
    def evaluate(self, results: list[Result]) -> Tuple[List[str], Dict[str, Tuple[int, int]]]:
        clean_payload_hits = []
        exploit_hit = {} #type exploit = (hits, total)

        for i, res in enumerate(results):
            #Check if clean payload hit
            if not res.applied_transforms:
                clean_payload_hits.append(res.payload)
                continue
    
            #checks for which exploits hit
            for transform, status in res.applied_transforms:
                for _, exploit in transform.exploits:
                    exploit_name = type(exploit).__name__
                    if exploit_name in exploit_hit:
                        hit_tuple = exploit_hit[exploit_name]
                        exploit_hit[exploit_name] = (hit_tuple[0]+1 if status else hit_tuple[0], hit_tuple[1]+1)
                    else:
                        exploit_hit[exploit_name] = (1 if status else 0, 1)
        return (clean_payload_hits, exploit_hit)
    
    def printEvaluation(self, evaluation: Tuple[List[str], Dict[str, Tuple[int, int]]]) -> None:
        clean_payload_hits, exploit_hits = evaluation
        print("\n--- RESULTS ---")
        print("Clean payloads hit: %i" % len(clean_payload_hits))
        for i, clean_payload in enumerate(clean_payload_hits):
            print("Payload %i: '%s'" % (i+1, clean_payload))
        
        if not exploit_hits.items(): 
            print("ALL PROMPTS HIT CLEAN \n NO EXPLOITS TESTED")
            return
        for exploit, tuple in exploit_hits.items():
            hits, total = tuple
            print("Exploit: %s - ASR %i (%i/%i)" % (exploit, (hits/total*100), hits, total))