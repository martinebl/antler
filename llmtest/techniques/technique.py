#!/usr/bin/env python3
import json
from enum import Enum
class TechniqueClass(Enum):
    SOCIAL_ENGINEERING = 1
    ESCAPING_USER_PROMPT = 2
    HIGHLIGHTING_IMPORTANCE = 3
    DESCRIBING_SHAPE_OF_OUTPUT = 4
    PROVIDING_CATALYST = 5
    FILTERING_UNWANTED_OUTPUT = 6
    IGNORING_RULES = 7
    CONTEXT_ENRICHMENT = 8
    OBFUSCATION_OF_OUTPUT = 9
    OBFUSCATION_OF_INPUT = 10
    OBFUSCATION_OF_INTENT = 11


class Technique:
    """Base class for applying an technique to a prompt/payload"""
    def __init__(self, tech_class: TechniqueClass) -> None:
        self.techniqueClass = tech_class

    def getTechniqueClass(self) -> TechniqueClass:
        return self.techniqueClass

    def applyTechnique(self, prompt: str) -> str:
        raise NotImplementedError("This method should be implemented by subclasses")
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self))
    
    #def isAnswerAffected
    def isAnswerAffected(self, prompt: str) -> bool:
        """
        Detect if the specific technique affected the answer in a way that might
        interfere with detection. Examples include encryption, translation or adding of spaces between characters.
        If this is the case, "cleanAffectedAnswer" should be called to restore the answer text to a "readable" format for detection.
        """
        return False
    
    def cleanAffectedAnswer(self, prompt: str) -> str:
        """
        The default implementation returns the prompt unchanged.
        """
        return prompt
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    


