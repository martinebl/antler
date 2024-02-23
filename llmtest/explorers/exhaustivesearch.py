import itertools
from llmtest.explorers import Explorer
from llmtest.exploits import Exploit
from llmtest.transforms import Transform

class ExhaustiveSearch(Explorer):
    """ This explorer class explores the space exhaustively. Only for use early, where few exploits are present """
    def __init__(self, exploits: list[Exploit]) -> None:
        super().__init__(exploits)

    def generateTransforms(self) -> list[Transform]:
        combos = [ itertools.combinations(self.exploits, i) for i in range(1, len(self.exploits) + 1) ]
        # The list that stores all the permutations, of all the combos
        perms = []
        for batch in combos:
            for combo in batch:
                # Append a list of permutations (which are themselves lists of exploits), for the given combination
                perms.append([ list(perm) for perm in itertools.permutations(combo)])
        
        return [ Transform(list(enumerate(permutation))) for perm_list in perms for permutation in perm_list ]