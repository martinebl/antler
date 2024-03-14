#!/usr/bin/env python3
import base64
from llmtest.techniques import *

class Encoding(Technique):
    def __init__(self) -> None:
        super().__init__(TechniqueClass.OBFUSCATION_OF_INPUT)

    def applyTechnique(self, prompt: str) -> str:
        # Remove the 'b' and enclosing quotes from the resulting string before returning it
        return str(base64.b64encode(prompt.encode('utf-8')))[2:-1]
    
    def affectedAnswer(self, prompt: str) -> bool:
        """
        Detect if the given answer is base64 encoded. This might sometimes give incorrect results
        """
        try:
            prompt_bytes = prompt.encode('utf-8')
            return base64.b64encode(base64.b64decode(prompt_bytes)) == prompt_bytes
        except Exception:
            # If there is an error trying to pass base64, then the answer is clearly not base64
            return False
    
    def decodeAnswer(self, prompt: str) -> str:
        return str(base64.b64decode(prompt.encode('utf-8')))[2:-1]