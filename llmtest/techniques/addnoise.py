#!/usr/bin/env python3
from llmtest.techniques import Technique

class AddNoise(Technique):
    def applyTechnique(self, prompt: str) -> str:
        return ' '.join(prompt)