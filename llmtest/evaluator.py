#!/usr/bin/env python3
from llmtest.result import Result
from llmtest.evaluation import Evaluation
from llmtest.attempt import Attempt

class Evaluator:
    def __init__(self) -> None:
        self = self

    def evaluate(self, attempts: list[Attempt]) -> Evaluation:
        techniques = {}
        transforms = {}
        probes = {}

        for attempt in attempts:
            probe_name = type(attempt.getProbe()).__name__

            # checks if transform is empty - only payload used in attempt
            if attempt.getTransform().isEmpty():
                #check if hit clean
                if attempt.getAttemptSuccessRate() >= 1: 
                    self.addToDict(probes, probe_name, -1)
                continue

            self.addToDict(probes, probe_name, attempt.getAttemptSuccessRate())
            
            transform_name = str(attempt.getTransform())
            self.addToDict(transforms, transform_name, attempt.getAttemptSuccessRate())

            for technique in attempt.getTransform().getExploits():
                technique_name = type(technique).__name__
                self.addToDict(techniques, technique_name, attempt.getAttemptSuccessRate())
        
        technique_results = self.createResultList(techniques)
        transform_results = self.createResultList(transforms)
        probe_results = self.createResultList(probes)

        return Evaluation(technique_results, transform_results, probe_results)

    def addToDict(self, dict:object, key:str, value:float):
        if not key in dict: dict[key] = []
        dict[key].append(value)

    def createResultList(self, dict:dict) -> list[Result]:
        results = []
        for name, score_list in dict.items():
            results.append(Result(name, score_list))
        return results


