#!/usr/bin/env python3
from llmtest.result import Result
from llmtest.evaluation import Evaluation
from llmtest.attempt import Attempt

class Evaluator:
    def __init__(self) -> None:
        self = self

    def evaluate(self, attempts: list[Attempt]) -> Evaluation:
        techniques: dict[str, list[float]] = {}
        transforms: dict[str, list[float]] = {}
        probes: dict[str, list[float]] = {}

        for attempt in attempts:

            # collecting probe scores
            probe_name = type(attempt.getProbe()).__name__
            if self.isEmptyTransform(attempt):
                if self.isCleanHit(attempt):
                    self.addToDict(probes, probe_name, -1)
                    continue
                else:
                    # discards empty transform non-clean probes
                    continue
            self.addToDict(probes, probe_name, attempt.getAttemptSuccessRate())

            # collecting transform scores
            transform_name = str(attempt.getTransform())
            self.addToDict(transforms, transform_name, attempt.getAttemptSuccessRate())

            # collecting technique scores
            for technique in attempt.getTransform().getExploits():
                technique_name = type(technique).__name__
                self.addToDict(techniques, technique_name, attempt.getAttemptSuccessRate())
        
        technique_results = self.createResultList(techniques)
        transform_results = self.createResultList(transforms)
        probe_results = self.createResultList(probes)

        return Evaluation(technique_results, transform_results, probe_results)


    def isEmptyTransform(self, attempt: Attempt) -> bool:
        return attempt.getTransform().isEmpty()
    
    def isCleanHit(self, attempt: Attempt) -> bool:
        return attempt.getAttemptSuccessRate() == 1


    def addToDict(self, dict:object, key:str, value:float):
        if not key in dict: dict[key] = []
        dict[key].append(value)

    def createResultList(self, dict:dict) -> list[Result]:
        results = []
        for name, score_list in dict.items():
            results.append(Result(name, score_list))
        return results
