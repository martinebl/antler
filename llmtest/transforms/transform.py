#!/usr/bin/env python3
from llmtest.exploits import Exploit
class Transform:
    """ 
    The base class for transforming a prompt, by applying exploits.
    """

    def __init__(self, exploits_with_priority: list[tuple[int, Exploit]]) -> None:
        self.exploits_with_priority = sorted(exploits_with_priority, key=lambda x: x[0])
        self.exploits = list(map(lambda x: x[1], self.exploits_with_priority))

    def applyExploits(self, payload: str) -> str:
        prompt = payload
        for exploit in self.exploits:
            prompt = exploit.applyExploit(prompt)
        return prompt
    
    def getExploits(self) -> list[Exploit]:
        return self.exploits
    
    def isEmpty(self) -> bool:
        return (True if len(self.exploits) == 0 else False)
    
    def __str__(self):
        str = ""
        for exploit in self.exploits:
            str += f"{type(exploit).__name__},"
        return f"({str})"
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Transform):
            return self.__dict__ == other.__dict__