#!/usr/bin/env python3
from llmtest.result import Result
from llmtest.evaluation import Evaluation

class Evaluator:
    def __init__(self) -> None:
        self = self

    #Every result = 1 probe
    def evaluate(self, results: list[Result]) -> Evaluation:
        clean_hit_payloads = []
        exploit_scores: dict[str, list[float]] = {}

        for res in results:
            # Checks for empty transformer - The transformer with clean hit prompts
            if len(res.transform.exploits) == 0:
                for probe in res.probes:
                    clean_hit_payloads.append(probe.getPayload())
                continue
            
            for _, exploit in res.transform.exploits:
                exploit_name = type(exploit).__name__
                if(exploit_name) in exploit_scores:
                    exploit_scores[exploit_name].append(res.score)
                else:
                    exploit_scores[exploit_name] = [res.score]
        return Evaluation(clean_hit_payloads, exploit_scores)