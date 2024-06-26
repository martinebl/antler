#!/usr/bin/env python3
import itertools
from antler.explorers import Explorer
from antler.techniques import Technique
from antler.transforms import Transform

class ExhaustiveSearch(Explorer):
    """ This explorer class explores the space exhaustively. Only for use early, where few techniques are present """
    def __init__(self, techniques: list[Technique], max_transforms: int) -> None:
        super().__init__(techniques, max_transforms)

    @staticmethod
    def generatePermutationsAndCombinations(techniques: list[Technique], min_length: int = 1, max_length: int = 5):
        combos = [ itertools.combinations(techniques, i) for i in range(min_length, min(len(techniques) + 1, max_length + 1)) ]
        # The list that stores all the permutations, of all the combos
        perms = []
        for batch in combos:
            for combo in batch:
                # Append a list of permutations (which are themselves lists of techniques), for the given combination
                perms.append([ list(perm) for perm in itertools.permutations(combo)])
        
        return [ Transform(permutation) for perm_list in perms for permutation in perm_list ]

    def generateInitialTransforms(self) -> list[Transform]:
        return self.generatePermutationsAndCombinations(self.techniques)
    
    def seedScore(self, result: float) -> None:
        pass