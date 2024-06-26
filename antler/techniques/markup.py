#!/usr/bin/env python3
from antler.techniques import Technique
from antler.techniques.technique import TechniqueClass

class Markup(Technique):
    def __init__(self) -> None:
        super().__init__(TechniqueClass.HIGHLIGHTING_IMPORTANCE)

    def applyTechnique(self, prompt: str) -> str:
        return f"***IMPORTANT NEW INSTRUCTIONS:***{prompt}***END NEW INSTRUCTIONS***"