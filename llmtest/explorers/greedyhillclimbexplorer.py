#!/usr/bin/env python3
from llmtest.explorers import Explorer
from llmtest.techniques import Technique
from llmtest.transforms import Transform

class GreedyHillClimbExplorer(Explorer):
    def __init__(self, techniques: list[Technique]) -> None:
        super().__init__(techniques)
        self.scores: list[tuple[Transform, float]] = []
        self.TRANSFORM_LENGTH_CAP = 5
        self.AMOUNT_OF_TOP_CANDIDATES = 10
        self.transform_length = 1

    def generateInitialTransforms(self) -> list[Transform]:
        """
        Generates a list of initial transforms, including only a single technique in each.
        """
        return [ Transform([technique]) for technique in self.techniques ]
    
    def seedScore(self, result: float) -> None:
        """
        Is used to keep track of the scores of each technique, and use that to explore the
        remaining possibilities
        """
        if self._index < len(self.transforms):
            # Append a tuple of (technique, score) to the scores array, while iterating
            # over all the techniques one at a time
            self.scores.append((self.transforms[self._index], result))
            # Handle the selection and transform generation on the last iteration of the single techniques
            if self._index == len(self.transforms) - 1 and self.transform_length < self.TRANSFORM_LENGTH_CAP:
                top_10_transform_scores = sorted(self.scores, key= lambda x: x[1], reverse=True)[:self.AMOUNT_OF_TOP_CANDIDATES]
                if(top_10_transform_scores[0][1] >= 1): 
                    self._setMessage(f"Local maximum found {top_10_transform_scores[0][0]}") 
                    return
                
                # explore next length of transforms
                self.__generateTransformsFromScores(top_10_transform_scores)
                self.transform_length += 1
                self._setMessage(f"Trying transforms of length {self.transform_length}")

    def __generateTransformsFromScores(self, scores) -> None:
        self.scores = []
        new_transforms = self.__incrementTransformsLength([tuple[0] for tuple in scores])
        
        self.transforms.extend(new_transforms)

    def __incrementTransformsLength(self, transforms: list[Transform]) -> list[Transform]:
        new_transforms = []

        for transform in transforms:
            techniques = transform.getTechniques()
            for technique in self.techniques:
                if technique not in techniques:
                    new_transforms.append(Transform(techniques + [technique]))

        return new_transforms