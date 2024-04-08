#!/usr/bin/env python3
from llmtest.explorers import Explorer
from llmtest.techniques import Technique, TechniqueClass
from llmtest.transforms import Transform
from llmtest.explorers.exhaustivesearch import ExhaustiveSearch

class SimulatedAnnealing(Explorer):
    def __init__(self, techniques: list[Technique]) -> None:
        super().__init__(techniques)
        self.best_techniques: list[Technique] = []
        self.scores: list[tuple[Technique, float]] = []

    def generateInitialTransforms(self) -> list[Transform]:
        """
        Generates a list of initial transforms, including only a single technique each.
        """
        return [ Transform([(1, technique)]) for technique in self.techniques ]
    
    def seedScore(self, result: float) -> None:
        """
        Is used to keep track of the scores of each technique, and use that to explore the
        remaining possibilities
        """
        if self._index < len(self.techniques):
            # Append a tuple of (technique, score) to the scores array, while iterating
            # over all the techniques one at a time
            self.scores.append((self.transforms[self._index].techniques[0], result))
            # Handle the selection and transform generation on the last iteration of the single techniques
            if self._index == len(self.techniques) - 1:
                self.best_techniques = self.__selectBestInClassTechniques()
                # self._setMessage("Trying generated transforms, from best in class techniques...")

    def __selectBestInClassTechniques(self) -> list[Technique]:
        """
        Get the top two techniques from each class
        """
        techniques_by_class = { tech_class:[] for tech_class in TechniqueClass }
        for technique, score in self.scores:
            tech_class = technique.getTechniqueClass()
            # Always append if list is empty
            if len(techniques_by_class[tech_class]) == 0:
                techniques_by_class[tech_class].append((technique, score))
            # Insert on appropriate place in the list, if necessary
            else:
                if techniques_by_class[tech_class][0][1] < score:
                    techniques_by_class[tech_class].insert(0, (technique, score))
                    techniques_by_class[tech_class] = techniques_by_class[tech_class][:2]
                elif techniques_by_class[tech_class][1][1] < score:
                    techniques_by_class[tech_class][1] = (technique, score)


        return list([technique for tech_scores in techniques_by_class.values() for technique, _ in tech_scores])
        
    


