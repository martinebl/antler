from llmtest.transforms import Transform
from llmtest.exploits import Exploit

class Explorer:
    """
    This is the base explorer class. This class defines how the search space
    of the permutations and combinations of exploits is explored.
    It is designed to work like an iterable wrapper around the list of transforms,
    so the list can be manipulated while iterating it.
    """
    
    def __init__(self, exploits: list[Exploit]) -> None:
        self.exploits = exploits
        self.index = -1 # So the first call to __next__ will be on index 0
        self.transforms = self.generateInitialTransforms()

    def __iter__(self):
        return self

    def __next__(self) -> Transform:
        self.index+=1
        try: # Uglier than counting the list on every run, but way more efficient
            return self.transforms[self.index]
        except IndexError:
            raise StopIteration
        
    def getTransforms(self):
        return self.transforms
    
    def generateInitialTransforms(self) -> list[Transform]:
        """
        The function to set the inital list of transforms. Could also be a list with one element.
        This list is iterated with the __next__ function, and possibly modified by the feedResult function.
        """
        raise NotImplementedError("This method should be implemented by subclasses")
    
    def feedResult(self, result: bool) -> None:
        """
        In the case of actual optimisation of exploration, this function is used to run the
        acquisition function of the bayesian optimisation, and append the next transform to
        try to the self.transforms list.
        """
        raise NotImplementedError("This method should be implemented by subclasses")