#!/usr/bin/env python3
from antler.result import Result
from antler.evaluation import Evaluation
from antler.attempt import Attempt

class Evaluator:
    def __init__(self) -> None:
        self = self

    def evaluate(self, attempts: list[Attempt]) -> Evaluation:
        # Each property is of the form dict[entry_name, list[tuple[succes_rate, succesfull_attempts, all_attempts]]]
        # The success_rate can be deduced from the following two, but is used right now with a negative value, to indicate a clean attempt
        techniques: dict[str, list[tuple[float, int, int]]] = {}
        transforms: dict[str, list[tuple[float, int, int]]] = {}
        probes: dict[str, list[tuple[float, int, int]]] = {}

        error_replies = 0
        total_replies = 0
        for attempt in attempts:

            # collecting error replies
            error_replies += sum(1 for reply in attempt.getReplies() if "error" in reply.keys())
            total_replies += len(attempt.getReplies())
            
            # collecting probe scores
            probe_name = type(attempt.getProbe()).__name__
            if self.isEmptyTransform(attempt):
                if self.isCleanHit(attempt):
                    Evaluator.addToDict(probes, probe_name, -1, attempt.getHitCount(), attempt.getNumberOfReplies())
                    continue
                else:
                    # discards empty transform non-clean probes
                    continue
            Evaluator.addToDict(probes, probe_name, attempt.getAttemptSuccessRate(), attempt.getHitCount(), attempt.getNumberOfReplies())

            # collecting transform scores
            transform_name = str(attempt.getTransform())
            Evaluator.addToDict(transforms, transform_name, attempt.getAttemptSuccessRate(), attempt.getHitCount(), attempt.getNumberOfReplies())

            # collecting technique scores
            for technique in attempt.getTransform().getTechniques():
                technique_name = type(technique).__name__
                Evaluator.addToDict(techniques, technique_name, attempt.getAttemptSuccessRate(), attempt.getHitCount(), attempt.getNumberOfReplies())
        
        unsorted_technique_results = self.createResultList(techniques)
        unsorted_transform_results = self.createResultList(transforms)
        unsorted_probe_results = self.createResultList(probes)
        transform_results = self.sortTransformResults(unsorted_transform_results)
        technique_results = sorted(unsorted_technique_results, key=lambda res: res.getScore(), reverse=True)
        probe_results = sorted(unsorted_probe_results, key=lambda res: res.getScore(), reverse=True)

        return Evaluation(technique_results, transform_results, probe_results, error_replies, total_replies)


    def isEmptyTransform(self, attempt: Attempt) -> bool:
        return attempt.getTransform().isEmpty()
    
    def isCleanHit(self, attempt: Attempt) -> bool:
        return attempt.getAttemptSuccessRate() == 1

    @staticmethod
    def addToDict(dict: object, key: str, succes_rate: float, succesful_attempts: int, all_attempts: int):
        if not key in dict: dict[key] = []
        dict[key].append((succes_rate, succesful_attempts, all_attempts))

    def createResultList(self, dict:dict) -> list[Result]:
        results = []
        for name, score_list in dict.items():
            results.append(Result(name, score_list))
        return results
    
    def sortTransformResults(self, transform_results: list[Result]):
        score_sorted = sorted(transform_results, key= lambda x: x.getScore(), reverse=True)
        combination_sorted = self.sortTransformResByCombination(score_sorted)
        return combination_sorted

    """ Sorting by combination has the sideeffect of messing length sorting up, since it compares alphabetically, therefore length sorting is applied at the end"""
    def sortTransformResByCombination(self, results: list[Result]) -> list[Result]:
        combination_sorted = sorted(results, key= lambda x: sorted(Evaluation.transformResultNameToArray(x.getName())))
        return self.sortTransformResByLen(combination_sorted)
    
    def sortTransformResByLen(self, results: list[Result]) -> list[Result]:
        return sorted(results, key= lambda x: len(Evaluation.transformResultNameToArray(x.getName())))


