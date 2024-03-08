#!/usr/bin/env python3
import base64
from llmtest.techniques import *

class Encoding(Technique):
    def __init__(self) -> None:
        super().__init__(TechniqueClass.OBFUSCATION_OF_INPUT)

    def applyTechnique(self, prompt: str) -> str:
        # Remove the 'b' and enclosing quotes from the resulting string before returning it
        return str(base64.b64encode(prompt.encode('utf-8')))[2:-1]