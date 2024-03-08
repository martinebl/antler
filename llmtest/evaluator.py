#!/usr/bin/env python3
from llmtest.result import Result
from llmtest.evaluation import Evaluation

class Evaluator:
    def __init__(self) -> None:
        self = self

    #Every result = 1 probe
    def evaluate(self, results: list[Result]) -> Evaluation:
        clean_hit_payloads = []
        technique_scores: dict[str, list[float]] = {}

        for res in results:
            # Checks for empty transformer - The transformer with clean hit prompts
            if len(res.transform.techniques) == 0:
                for probe in res.probes:
                    clean_hit_payloads.append(probe.getPayload())
                continue
            
            for technique in res.transform.techniques:
                technique_name = type(technique).__name__
                if(technique_name) in technique_scores:
                    technique_scores[technique_name].append(res.score)
                else:
                    technique_scores[technique_name] = [res.score]
        return Evaluation(clean_hit_payloads, technique_scores)