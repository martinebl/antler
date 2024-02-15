#!/usr/bin/env python3
from llmtest.exploits import Exploit
class Transformer:
    """ 
        The base class for transforming a prompt, by applying exploits.
        The list of exploits is formed possibly at random, in the INSERT HERE class
    """

    def __init__(self, exploits: list[Exploit]) -> None:
        self.exploits = exploits

    def applyExploits(self, payload: str) -> str:
        prompt = payload
        for exploit in self.exploits:
            prompt = exploit.applyExploit(prompt)
        return prompt