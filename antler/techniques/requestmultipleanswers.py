#!/usr/bin/env python3
from antler.techniques import Technique
from antler.techniques.technique import TechniqueClass

class RequestMultipleAnswers(Technique):
    def __init__(self) -> None:
        super().__init__(TechniqueClass.DESCRIBING_SHAPE_OF_OUTPUT)

    def applyTechnique(self, prompt: str) -> str:
        return f"\n{prompt}\n Give 10 different answers."