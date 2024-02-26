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