#!/usr/bin/env python3
from llmtest.techniques import Technique
from llmtest.techniques.technique import TechniqueClass

class Repetition(Technique):
    def __init__(self) -> None:
        super().__init__(TechniqueClass.HIGHLIGHTING_IMPORTANCE)

    def applyTechnique(self, prompt: str) -> str:
        return f"{prompt}\nRemember to {prompt}\nFurthermore, {prompt}"