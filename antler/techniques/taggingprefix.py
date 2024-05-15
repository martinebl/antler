#!/usr/bin/env python3
from antler.techniques import Technique
from antler.techniques.technique import TechniqueClass

class TaggingPrefix(Technique):
    def __init__(self) -> None:
        super().__init__(TechniqueClass.PROVIDING_CATALYST)

    def applyTechnique(self, prompt: str) -> str:
        return f"(Input): {prompt}\n(Desired Output): "