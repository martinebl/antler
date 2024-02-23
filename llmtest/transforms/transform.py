#!/usr/bin/env python3
from llmtest.exploits import Exploit
class Transform:
    """ 
    The base class for transforming a prompt, by applying exploits.
    """

    def __init__(self, exploits: list[(int, Exploit)]) -> None:
        self.exploits = sorted(exploits, key=lambda x: x[0])

    def applyExploits(self, payload: str) -> str:
        prompt = payload
        for tuple in self.exploits:
            prompt = tuple[1].applyExploit(prompt)
        return prompt