#!/usr/bin/env python3
from llmtest.techniques import Technique
class Transform:
    """ 
    The base class for transforming a prompt, by applying techniques.
    """

    def __init__(self, techniques_with_priority: list[tuple[int, Technique]]) -> None:
        self.techniques_with_priority = sorted(techniques_with_priority, key=lambda x: x[0])
        self.techniques = list(map(lambda x: x[1], self.techniques_with_priority))

    def applyTechniques(self, payload: str) -> str:
        prompt = payload
        for technique in self.techniques:
            prompt = technique.applyTechnique(prompt)
        return prompt