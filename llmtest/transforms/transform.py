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
    
    def getTechniques(self) -> list[Technique]:
        return self.techniques
    
    def isEmpty(self) -> bool:
        return (True if len(self.techniques) == 0 else False)
    
    def __str__(self):
        str = ""
        for technique in self.techniques:
            str += f"{type(technique).__name__},"
        return f"({str})"
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Transform):
            return self.__dict__ == other.__dict__
        
        
