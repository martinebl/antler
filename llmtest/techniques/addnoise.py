#!/usr/bin/env python3
from llmtest.techniques import *

class AddNoise(Technique):
    def __init__(self) -> None:
        super().__init__(TechniqueClass.OBFUSCATION_OF_INPUT)

    def applyTechnique(self, prompt: str) -> str:
        return ' '.join(prompt)