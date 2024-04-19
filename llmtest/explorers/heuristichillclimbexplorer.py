#!/usr/bin/env python3
from llmtest.explorers import Explorer
from llmtest.techniques import Technique
from llmtest.transforms import Transform
from llmtest.explorers.exhaustivesearch import ExhaustiveSearch
from llmtest.jsonparser import JSONParser
from llmtest.filehandler import Filehandler
from llmtest.evaluator import Evaluator
from llmtest.evaluation import Evaluation

import sys

class HeuristicHillClimbExplorer(Explorer):
    def __init__(self, techniques: list[Technique]) -> None:
        self.__scores: list[tuple[Transform, float]] = []
        self.__isHeuristicDone = False

        self.__HEURISTIC: list[tuple[Transform, float]] = []
        self.__static_candidate_index = 0
        self.__MAX_CANDIDATE = 3
        self.__candidate_heuristic: list[tuple[Transform, float]] = []

        self.__RUN_LIMIT = 130

        self.__last_scoring: tuple[Transform, float] = (Transform([]), -1)
        super().__init__(techniques)

    def setHeuristic(self, heuristic: list[tuple[Transform, float]]):
        self.__heuristic = heuristic

    def getHeuristic(self) -> list[tuple[Transform, float]]:
        return self.__heuristic

    def generateInitialTransforms(self) -> list[Transform]:
        """
        Generates a list of initial transforms, including only a single technique in each.
        """ 
        #return self.preLoadHeuristic()
        return ExhaustiveSearch.generatePermutationsAndCombinations(self.techniques, 2, 2)
    
    def selectStartingPoint(self) -> tuple[Transform, float]:
        starting_point = self.__heuristic.pop(0)
        self.__heuristic = [tup for tup in self.__heuristic if not starting_point[0].isSameCombination(tup[0])]
        return starting_point

    def selectBestHeuristic(self, transform: Transform) -> tuple[Transform, bool]:
        bestMatchIndex = sys.maxsize
        prepend = False
        for technique in transform.getTechniques():
            next_occurence = next((i for i, tup in enumerate(self.__heuristic) if technique in tup[0].getTechniques()), sys.maxsize)
            if bestMatchIndex > next_occurence:
                bestMatchIndex = next_occurence
                prepend = False if technique == self.__heuristic[bestMatchIndex][0].getTechniques()[0] else True 
        # exhausted search for current candidate
        if bestMatchIndex == sys.maxsize or len(self.__heuristic) == 0:
            return None
        return (self.__heuristic.pop(bestMatchIndex)[0], prepend)

    def __extendTransform(self, transform: Transform, extension: Transform):
        prepend: bool = False if extension[0] in transform.getTechniques() else True
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
        for i in range(len(candidate_index) + 1):
            heuristic.pop(i)

    def __removeSameCombinationTransforms(self, heuristic: list[tuple[Transform, float]], transform:Transform):
        return [tup for tup in heuristic if not transform.isSameCombination(tup[0])]

    def __initializeFreshCandidate(self):
        transform, score = self.__getCurrentCandidate()
        self.__candidate_heuristic = self.__HEURISTIC.copy()
        self.__removeAllCandidates(self.__candidate_heuristic, self.__static_candidate_index)
        self.__removeSameCombinationTransforms(self.__candidate_heuristic, transform)
        return (transform, score)

    def __setLastScoring(self, scoring: tuple[Transform, float]) -> None:
        self.__last_scoring = scoring

    def __findBestExtension(self, heuristic:list[tuple[Transform, float]], candidate_transform: Transform) -> Transform:
        for transform in [scoring[0] for scoring in heuristic]:
            for technique in candidate_transform.getTechniques():
                if technique in transform.getTechniques():
                    extension = transform
                    return extension
        return None

    def seedScore(self, result: float) -> None:
        print("HERE")
        """
        Is used to keep track of the scores of each technique, and use that to explore the
        remaining possibilities
        """
        if self._index >= self.__RUN_LIMIT: return

        last_transform, last_score = self.__last_scoring
        current_transform: Transform = self.transforms[self._index]
        current_score: float = result
        current_scoring: tuple[Transform, float] = (current_transform, current_score)
        new_transform: Transform

        if not self.__isHeuristicDone:
            self.__scores.append(current_transform, current_score)
            if self.__initialTransformsForHeuristicFinished():
                self.__initializeHeuristic(self.__scores)
                current_transform, current_score = self.__initializeFreshCandidate()
            self._setMessage(f"Constructing heuristic...")
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
        extension = self.__findBestExtension(current_candidate)

        while extension is None and self.__static_candidate_index < self.__MAX_CANDIDATE:
            self.__static_candidate_index += 1
            fresh_candidate_scoring = self.__initializeFreshCandidate()
            self.__setLastScoring(fresh_candidate_scoring)
            current_candidate = fresh_candidate_scoring[0]
            extension = self.__findBestExtension(fresh_candidate_scoring[0])
        
        if extension is None: return

        new_transform = self.__extendTransform(current_candidate, extension)
        self.transforms.append(new_transform)
            
        self._setMessage(f"Trying transform {new_transform}")

    def preLoadHeuristic(self) -> list[Transform]:
        """
        Used to load in heuristic from a file instead of an active run
        """
        file_path = "named_logs/mistral_exhaustivesearch.json"
        json_data = Filehandler.read_json_file(file_path)
        if json_data is not None:
            attempts = JSONParser.parse_json_as_attempts(json_data["attempts"])

            eval: Evaluation = Evaluator().evaluate(attempts)
            scores: list[tuple[Transform, float]] = [(JSONParser.transform_name_to_transform(res.getName()), res.getScore()) for res in eval.transform_results_original]
            self.__initializeHeuristic(scores)
            scoring = self.__initializeFreshCandidate()
            self.__last_scoring = scoring
            extension = self.__findBestExtension(scoring[0])


            return [self.__extendTransform(scoring[0], extension)]

        print("Heuristic DID NOT preload")