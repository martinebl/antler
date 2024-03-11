#!/usr/bin/env python3
from llmtest.result import Result
from llmtest.evaluation import Evaluation
from llmtest.attempt import Attempt

class Evaluator:
    def __init__(self) -> None:
        self = self

    def evaluate(self, attempts: list[Attempt]) -> Evaluation:
        # Each property is of the form dict[entry_name, list[tuple[succes_rate, succesfull_attempts, all_attempts]]]
        # The success_rate can be deduced from the following two, but is used right now with a negative value, to indicate a clean attempt
        techniques: dict[str, list[tuple[float, int, int]]] = {}
        transforms: dict[str, list[tuple[float, int, int]]] = {}
        probes: dict[str, list[tuple[float, int, int]]] = {}

        for attempt in attempts:

            # collecting probe scores
            probe_name = type(attempt.getProbe()).__name__
            if self.isEmptyTransform(attempt):
                if self.isCleanHit(attempt):
                    self.addToDict(probes, probe_name, -1, attempt.getHitCount(), attempt.getNumberOfReplies())
                    continue
                else:
                    # discards empty transform non-clean probes
                    continue
            self.addToDict(probes, probe_name, attempt.getAttemptSuccessRate(), attempt.getHitCount(), attempt.getNumberOfReplies())

            # collecting transform scores
            transform_name = str(attempt.getTransform())
            self.addToDict(transforms, transform_name, attempt.getAttemptSuccessRate(), attempt.getHitCount(), attempt.getNumberOfReplies())

            # collecting technique scores
            for technique in attempt.getTransform().getTechniques():
                technique_name = type(technique).__name__
                self.addToDict(techniques, technique_name, attempt.getAttemptSuccessRate(), attempt.getHitCount(), attempt.getNumberOfReplies())
        
        technique_results = self.createResultList(techniques)
        transform_results = self.createResultList(transforms)
        probe_results = self.createResultList(probes)

        return Evaluation(technique_results, transform_results, probe_results)


    def isEmptyTransform(self, attempt: Attempt) -> bool:
        return attempt.getTransform().isEmpty()
    
    def isCleanHit(self, attempt: Attempt) -> bool:
        return attempt.getAttemptSuccessRate() == 1


    def addToDict(self, dict: object, key: str, succes_rate: float, succesful_attempts: int, all_attempts: int):
        if not key in dict: dict[key] = []
        dict[key].append((succes_rate, succesful_attempts, all_attempts))

    def createResultList(self, dict:dict) -> list[Result]:
        results = []
        for name, score_list in dict.items():
            results.append(Result(name, score_list))
        return results
