#!/usr/bin/env python3
from llmtest.explorers import Explorer
from llmtest.techniques import Technique
from llmtest.transforms import Transform
from llmtest.explorers.exhaustivesearch import ExhaustiveSearch

class ClassExplorer(Explorer):
    def __init__(self, techniques: list[Technique]) -> None:
        super().__init__(techniques)

    def generateInitialTransforms(self) -> list[Transform]:
        """
        Generates a list of all transforms, consisting of only techniques from within the same classes
        """
        grouped = {}
        result: list[Transform] = []
        # Group techniques by class
        for technique in self.techniques:
            tech_class = technique.getTechniqueClass()
            if tech_class not in grouped.keys():
                grouped[tech_class] = [technique]
            else:
                grouped[tech_class].append(technique)
        # Generate transforms
        for tech_class, techniques in grouped.items():
            result.extend(ExhaustiveSearch.generatePermutationsAndCombinations(techniques, max_length=len(techniques)))
        
        return result
    
    def seedScore(self, result: float) -> None:
        pass

