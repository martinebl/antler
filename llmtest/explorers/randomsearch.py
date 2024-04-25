#!/usr/bin/env python3
import random

from llmtest.explorers import Explorer
from llmtest.techniques import Technique
from llmtest.transforms import Transform

class RandomSearch(Explorer):
    """ This explorer class explores the space exhaustively. Only for use early, where few techniques are present """
    def __init__(self, techniques: list[Technique]) -> None:
        self.min_transform_length = 2
        self.max_transform_length = 8
        self.current_iteration = -1
        self.max_iterations = 100
        self.stop_score = 1
        super().__init__(techniques)


    def __len__(self) -> int:
        return self.max_iterations

    def __generateRandomTransform(self) -> Transform:
        return Transform(list(random.sample(self.techniques, random.randint(min(self.min_transform_length, len(self.techniques)), min(self.max_transform_length, len(self.techniques))))))

    def generateInitialTransforms(self) -> list[Transform]:
        return [self.__generateRandomTransform()]
    
    def seedScore(self, score: float) -> None:
        self.current_iteration += 1
        if self.current_iteration >= (self.max_iterations - 1):
            return
        elif score >= self.stop_score:
            self._setMessage("Found satisfying score, terminating early")
            return
        else:
            self.transforms.append(self.__generateRandomTransform())