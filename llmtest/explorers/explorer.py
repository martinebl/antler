from llmtest.transforms import Transform
from llmtest.exploits import Exploit

class Explorer:
    """ This is the base explorer class. This class defines how the search space
        of the permutations and combinations of exploits is explored """
    
    def __init__(self, exploits: list[Exploit]) -> None:
        self.exploits = exploits


    def generateTransforms(self) -> list[Transform]:
        raise NotImplementedError("This method should be implemented by subclasses")