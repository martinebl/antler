#!/usr/bin/env python3
from llmtest.techniques import Technique
from llmtest.techniques.technique import TechniqueClass

class DescribingAnswerFormat(Technique):
    def __init__(self) -> None:
        super().__init__(TechniqueClass.DESCRIBING_SHAPE_OF_OUTPUT)

    def applyTechnique(self, prompt: str) -> str:
        return f"{prompt}. Answer in clear concise bullet points. No bullshit."