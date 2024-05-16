#!/usr/bin/env python3
from antler.explorers import Explorer
from antler.techniques import Technique
from antler.transforms import Transform
from antler.explorers.exhaustivesearch import ExhaustiveSearch

class HeuristicHillClimbExplorer(Explorer):
    def __init__(self, techniques: list[Technique], max_transforms: int) -> None:
        self.__scores: list[tuple[Transform, float]] = []
        self.__isHeuristicDone = False

        self.__HEURISTIC: list[tuple[Transform, float]] = []
        self.__static_candidate_index = 0
        self.__MAX_CANDIDATE = 3
        self.__candidate_heuristic: list[tuple[Transform, float]] = []

        self.__last_scoring: tuple[Transform, float] = (Transform([]), -1)
        super().__init__(techniques, max_transforms)

    def setHeuristic(self, heuristic: list[tuple[Transform, float]]):
        self.__candidate_heuristic = heuristic

    def setNoneCandidateHeuristic(self, heuristic: list[tuple[Transform, float]]):
        self.__HEURISTIC = heuristic

    def getHeuristic(self) -> list[tuple[Transform, float]]:
        return self.__candidate_heuristic

    def generateInitialTransforms(self) -> list[Transform]:
        """
        Generates a list of initial transforms, including only a single technique in each.
        """ 
        self._setMessage(f"Constructing heuristic...")
        return ExhaustiveSearch.generatePermutationsAndCombinations(self.techniques, 2, 2)

    def __extendTransform(self, transform: Transform, extension: Transform) -> Transform:
        prepend: bool = False if extension.getTechniques()[0] in transform.getTechniques() else True
        if prepend:
            techniques = [extension.getTechniques()[0]] + transform.getTechniques()
        else:
            techniques = transform.getTechniques() + [extension.getTechniques()[1]]
        new_transform = Transform(techniques)
        return new_transform

    def __initializeHeuristic(self, scores: list[tuple[Transform, float]]) -> None:
        self.__HEURISTIC = sorted([tup for tup in scores if len(tup[0].getTechniques()) == 2], key= lambda x: x[1], reverse= True)
    
    def __isGlobalMax(self, score: float) -> bool:
        return score >= 1

    def __initialTransformsForHeuristicFinished(self) -> bool:
        return self._index == len(self.transforms) - 1

    def __getCurrentCandidate(self) -> tuple[Transform, float]:
        return self.__HEURISTIC[self.__static_candidate_index]

    def __removeAllCandidates(self, heuristic: list[tuple[Transform, float]], candidate_index):
        return heuristic[candidate_index+1:]

    @staticmethod
    def __removeSameCombinationTransforms(heuristic: list[tuple[Transform, float]], transform:Transform):
        return [tup for tup in heuristic if not transform.isSameCombination(tup[0])]
    
    @staticmethod
    def __removeTransformFromHeuristic(heuristic:list[tuple[Transform, float]], transform:Transform):
        return [scoring for scoring in heuristic if scoring[0] != transform]

    def __initializeFreshCandidate(self):
        transform, score = self.__getCurrentCandidate()
        self.__candidate_heuristic = self.__HEURISTIC.copy()
        self.__candidate_heuristic = self.__removeAllCandidates(self.__candidate_heuristic, self.__static_candidate_index)
        self.__candidate_heuristic = HeuristicHillClimbExplorer.__removeSameCombinationTransforms(self.__candidate_heuristic, transform)
        return (transform, score)

    def __setLastScoring(self, scoring: tuple[Transform, float]) -> None:
        self.__last_scoring = scoring

    def __findBestExtension(self, heuristic:list[tuple[Transform, float]], candidate_transform: Transform) -> Transform:
        for transform in [scoring[0] for scoring in heuristic]:
            for technique in candidate_transform.getTechniques():
                if technique == transform.getTechniques()[0] and transform.getTechniques()[1] not in candidate_transform.getTechniques():
                    extension = transform
                    return extension
                if technique == transform.getTechniques()[1] and transform.getTechniques()[0] not in candidate_transform.getTechniques():
                    extension = transform
                    return extension

        return None


    def seedScore(self, result: float) -> None:
        """
        Is used to keep track of the scores of each technique, and use that to explore the
        remaining possibilities
        """

        last_transform, last_score = self.__last_scoring
        current_transform: Transform = self.transforms[self._index]
        current_score: float = result
        current_scoring: tuple[Transform, float] = (current_transform, current_score)
        new_transform: Transform

        if not self.__isHeuristicDone:
            self.__scores.append((current_transform, current_score))
            if self.__initialTransformsForHeuristicFinished():
                self.__initializeHeuristic(self.__scores)
                self.__isHeuristicDone = True
                current_transform, current_score = self.__initializeFreshCandidate()
            else:
                return

        if self.__isGlobalMax(current_score): 
            self._setMessage(f"Maximum found {current_transform}")
            return 
        
        current_candidate: Transform
        if current_score > last_score:
            current_candidate = current_transform
            self.__setLastScoring(current_scoring)
        else:
            current_candidate = last_transform
        extension = self.__findBestExtension(self.__candidate_heuristic, current_candidate)

        while extension is None and self.__static_candidate_index < self.__MAX_CANDIDATE:
            self.__static_candidate_index += 1
            fresh_candidate_scoring = self.__initializeFreshCandidate()
            self.__setLastScoring(fresh_candidate_scoring)
            current_candidate = fresh_candidate_scoring[0]
            extension = self.__findBestExtension(self.__candidate_heuristic, fresh_candidate_scoring[0])
        
        if extension is None: return
        self.__candidate_heuristic = self.__removeTransformFromHeuristic(self.__candidate_heuristic, extension)

        new_transform = self.__extendTransform(current_candidate, extension)
        self.transforms.append(new_transform)
        self._setMessage(f"Trying transform {new_transform} from {current_candidate} & {extension}")