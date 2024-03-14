#!/usr/bin/env python3
import re

from llmtest.techniques import *


class AddNoise(Technique):
    def __init__(self) -> None:
        super().__init__(TechniqueClass.OBFUSCATION_OF_INPUT)

    def applyTechnique(self, prompt: str) -> str:
        return ' '.join(prompt)
    
    def isAnswerAffected(self, prompt: str) -> bool:
        return True if re.search(r"\w\w", prompt) == None else False
    
    def cleanAffectedAnswer(self, prompt: str) -> str:
        # Replace tripple spaces with a rare marker, to replace with single space later
        temp = prompt.replace("   ", "½")
        
        temp = temp.replace(" ", "")
        return temp.replace("½", " ")