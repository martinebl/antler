#!/usr/bin/env python3
from llmtest.explorers import Explorer
from llmtest.techniques import Technique
from llmtest.transforms import Transform
from llmtest.explorers.exhaustivesearch import ExhaustiveSearch

class BestInClassExplorer(Explorer):
    def __init__(self, techniques: list[Technique]) -> None:
        super().__init__(techniques)
        self.scores: list[tuple[Technique, float]] = []
        self.best_class_techniques: list[Technique] = []
        self._setMessage("Trying techniques individually...")

    def generateInitialTransforms(self) -> list[Transform]:
        """
        Generates a list of initial transforms, including only a single technique in each.
        """
        return [ Transform([(1, technique)]) for technique in self.techniques ]
    
    def seedScore(self, result: float) -> None:
        """
        Is used to keep track of the scores of each technique, and use that to explore the
        remaining possibilities
        """
        if self.index < len(self.techniques):
            # Append a tuple of (technique, score) to the scores array, while iterating
            # over all the techniques one at a time
            self.scores.append((self.transforms[self.index].techniques[0], result))
            # Handle the selection and transform generation on the last iteration of the single techniques
            if self.index == len(self.techniques) - 1:
                self.__generateTransformsFromScores()
                self._setMessage("Trying generated transforms, from best in class techniques...")
    
    def __generateTransformsFromScores(self) -> None:
        #Firstly get all transforms from each class, with the best score
        techniques_by_class = {}
        for technique, score in self.scores:
            tech_class = technique.getTechniqueClass()
            if tech_class not in techniques_by_class or techniques_by_class[tech_class][1] < score:
                techniques_by_class[tech_class] = (technique, score)

        best_in_class = list([technique for technique, _ in techniques_by_class.values()])
        self.transforms.extend(ExhaustiveSearch.generatePermutationsAndCombinations(best_in_class, 2, 3))

