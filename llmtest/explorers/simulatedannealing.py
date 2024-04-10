#!/usr/bin/env python3
import random

from llmtest.explorers import Explorer
from llmtest.techniques import Technique, TechniqueClass
from llmtest.transforms import Transform
from llmtest.explorers.exhaustivesearch import ExhaustiveSearch

class SimulatedAnnealing(Explorer):
    def __init__(self, techniques: list[Technique]) -> None:
        super().__init__(techniques)
        self.best_techniques: list[Technique] = []
        self.scores: list[tuple[Technique, float]] = []
        self.start_temperature = 2
        self.max_iterations = 200
        self.current_transform = None # This is the current state
        self.current_score = 0.0 # This is the current "energy"
        self.best_transform = None # Used for restarts, if no better one has been found in a while
        self.best_score = 0.0 # Used for restarts.
        self._setMessage("Trying techniques individually...")

    def __len__(self) -> int:
        return self.max_iterations + len(self.techniques)

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
                self._setMessage("Starting simulated annealing from top 2 techniques in each class")
                self.best_techniques = self.__selectBestInClassTechniques()
                # TODO: Initialise annealing. Probably by creating a random transform, or combining the n best ones

        else:
            # TODO: Do annealing stuff
            return

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
        
    def __chooseNeighbour(self, temperature: float, transform) -> Transform:
        # Take a sample and scale it down with the temperature "progress"
        sample = random.random() * (temperature/self.start_temperature) 
        # The probabilities of doing the transforms in order: Swap cons, Swap non cons, Exchange in class, Exchange outside class
        probabilities = [0.2, 0.2, 0.3, 0.3]
        if sample > sum(probabilities[:3]):
            # Exchange a random technique, with one from another class
            new_transform = self.__exchangeFromOutsideClass(transform)
        elif sample > sum(probabilities[:2]):
            # Exchange a random technique, with one from same class
            new_transform = self.__exchangeFromSameClass(transform)
        elif sample > probabilities[0]:
            # Swap to random, non consecutive techniques
            new_transform = self.__swapNonConsecutive(transform)
        else:
            # Swap two consecutive techniques
            new_transform = self.__swapConsecutive(transform)

        return new_transform
    
    def exchangeFromOutsideClass(self, transform: Transform) -> Transform:
        transform_techniques = transform.getTechniques().copy()
        # Choose random index
        index = random.randint(0, len(transform_techniques) - 1)
        tech_class = transform_techniques[index].getTechniqueClass()
        # Select a random new technique, from 
        new_technique = random.choice(list(filter(lambda x: x.getTechniqueClass() != tech_class, self.best_techniques)))
        # Overwrite the new technique at index
        transform_techniques[index] = new_technique
        return Transform([ (1, technique) for technique in transform_techniques])
    
    def __exchangeFromSameClass(self, transform: Transform) -> Transform:
        return transform
    
    def __swapNonConsecutive(self, transform: Transform) -> Transform:
        return transform
    
    def __swapConsecutive(self, transform: Transform) -> Transform:
        return transform
