#!/usr/bin/env python3
from antler.techniques import Technique
from antler.techniques.technique import TechniqueClass

CHARACTER_MAP = {
    'a': '\U000E0061',
    'b': '\U000E0062',
    'c': '\U000E0063',
    'd': '\U000E0064',
    'e': '\U000E0065',
    'f': '\U000E0066',
    'g': '\U000E0067',
    'h': '\U000E0068',
    'i': '\U000E0069',
    'j': '\U000E006A',
    'k': '\U000E006B',
    'l': '\U000E006C',
    'm': '\U000E006D',
    'n': '\U000E006E',
    'o': '\U000E006F',
    'p': '\U000E0070',
    'q': '\U000E0071',
    'r': '\U000E0072',
    's': '\U000E0073',
    't': '\U000E0074',
    'u': '\U000E0075',
    'v': '\U000E0076',
    'w': '\U000E0077',
    'x': '\U000E0078',
    'y': '\U000E0079',
    'z': '\U000E007A',
    'A': '\U000E0041',
    'B': '\U000E0042',
    'C': '\U000E0043',
    'D': '\U000E0044',
    'E': '\U000E0045',
    'F': '\U000E0046',
    'G': '\U000E0047',
    'H': '\U000E0048',
    'I': '\U000E0049',
    'J': '\U000E004A',
    'K': '\U000E004B',
    'L': '\U000E004C',
    'M': '\U000E004D',
    'N': '\U000E004E',
    'O': '\U000E004F',
    'P': '\U000E0050',
    'Q': '\U000E0051',
    'R': '\U000E0052',
    'S': '\U000E0053',
    'T': '\U000E0054',
    'U': '\U000E0055',
    'V': '\U000E0056',
    'W': '\U000E0057',
    'X': '\U000E0058',
    'Y': '\U000E0059',
    'Z': '\U000E005A',
}

class InvisibleCharacters(Technique):
    def __init__(self) -> None:
        super().__init__(TechniqueClass.OBFUSCATION_OF_INPUT)

    def applyTechnique(self, prompt):
        return ''.join(CHARACTER_MAP.get(character, character) for character in prompt)
