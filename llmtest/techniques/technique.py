#!/usr/bin/env python3
from enum import Enum
class Technique:
    """Base class for applying an technique to a prompt/payload"""

    def applyTechnique(self, prompt: str) -> str:
        raise NotImplementedError("This method should be implemented by subclasses")
    

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


