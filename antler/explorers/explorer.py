from antler.transforms import Transform
from antler.techniques import Technique

class Explorer:
    """
    This is the base explorer class. This class defines how the search space
    of the permutations and combinations of techniques is explored.
    It is designed to work like an iterable wrapper around the list of transforms,
    so the list can be manipulated while iterating it.
    """
    
    def __init__(self, techniques: list[Technique], max_transforms: int) -> None:
        self.techniques = techniques
        self._index = -1 # So the first call to __next__ will be on index 0
        self.transforms = self.generateInitialTransforms()
        self.__hasMessage = False
        self.__message = ""
        self.max_transforms = max_transforms

    def __iter__(self):
        return self
    
    def hasMessage(self) -> bool:
        return self.__hasMessage
    
    def getMessage(self) -> str:
        self.__hasMessage = False
        return self.__message
    
    def _setMessage(self, message: str) -> None:
        self.__hasMessage = True
        self.__message = message

    def __next__(self) -> Transform:
        self._index+=1
        if (self._index >= (self.max_transforms)):
            raise StopIteration
        try: # Uglier than counting the list on every run, but way more efficient
            return self.transforms[self._index]
        except IndexError:
            raise StopIteration
        
    def __len__(self) -> int:
        return self.max_transforms
        
    def getTransforms(self):
        return self.transforms
    
    def generateInitialTransforms(self) -> list[Transform]:
        """
        The function to set the inital list of transforms. Could also be a list with one element.
        This list is iterated with the __next__ function, and possibly modified by the seedScore function.
        """
        raise NotImplementedError("This method should be implemented by subclasses")
    
    def seedScore(self, score: float) -> None:
        """
        In the case of actual optimisation of exploration, this function is used to run the
        acquisition function of the bayesian optimisation, and append the next transform to
        try to the self.transforms list.
        """
        raise NotImplementedError("This method should be implemented by subclasses")