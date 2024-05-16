#!/usr/bin/env python3
import random

from antler.explorers import Explorer
from antler.techniques import Technique
from antler.transforms import Transform

class RandomSearch(Explorer):
    """ This explorer class explores the space completely randomly. """
    def __init__(self, techniques: list[Technique], max_transforms: int) -> None:
        self.min_transform_length = 2
        self.max_transform_length = 8
        self.current_iteration = -1
        self.stop_score = 1
        super().__init__(techniques, max_transforms)

    def __generateRandomTransform(self) -> Transform:
        return Transform(list(random.sample(self.techniques, random.randint(min(self.min_transform_length, len(self.techniques)), min(self.max_transform_length, len(self.techniques))))))

    def generateInitialTransforms(self) -> list[Transform]:
        return [self.__generateRandomTransform()]
    
    def seedScore(self, score: float) -> None:
        self.current_iteration += 1
        if score >= self.stop_score:
            self._setMessage("Found satisfying score, terminating early")
            return
        else:
            self.transforms.append(self.__generateRandomTransform())