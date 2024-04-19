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
        self.__heuristic: list[tuple[Transform, float]] = []
        self.__RUN_LIMIT = 130
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
        if bestMatchIndex == sys.maxsize or len(self.__heuristic) == 0:
            return None
        return (self.__heuristic.pop(bestMatchIndex)[0], prepend)

    def extendTransform(self, transform: Transform, extension: Transform, prepend: bool):
        if prepend:
            techniques = [extension.getTechniques()[0]] + transform.getTechniques()
        else:
            techniques = transform.getTechniques() + [extension.getTechniques()[1]]
        new_transform = Transform(techniques)
        return new_transform

    def setupHeuristic(self, scores: list[tuple[Transform, float]]) -> Transform:
        self.__heuristic = sorted([tup for tup in scores if len(tup[0].getTechniques()) == 2], key= lambda x: x[1], reverse= True)
        startingPoint = self.selectStartingPoint()
        self.__last: tuple[Transform, float] = startingPoint
        transform = startingPoint[0]
        extension, prepend = self.selectBestHeuristic(transform)
        start_transform = self.extendTransform(transform, extension, prepend)
        return start_transform

    def seedScore(self, result: float) -> None:
        """
        Is used to keep track of the scores of each technique, and use that to explore the
        remaining possibilities
        """
        if self._index < len(self.transforms) and self._index < self.__RUN_LIMIT:
            if not self.__isHeuristicDone:
                self.__scores.append((self.transforms[self._index], result))
                if self._index == len(self.transforms) - 1:
                    self.__isHeuristicDone = True
                    start_transform = self.setupHeuristic(self.__scores)
                    self.transforms.append(start_transform)
                    return
                return
            
            if(result >= 1):
                self._setMessage(f"Local maximum found {self.transforms[self._index]}")
                return
            if(result >= self.__last[1]):
                self.__last = (self.transforms[self._index], result)
                tuple = self.selectBestHeuristic(self.transforms[self._index])
                if not tuple: 
                    self._setMessage(f"Exhausted search - exiting")
                    return 
                extension, prepend = tuple
                new_transform = self.extendTransform(self.transforms[self._index], extension, prepend)
                self.transforms.append(new_transform)
            else:
                tuple = self.selectBestHeuristic(self.__last[0])
                if not tuple: 
                    self._setMessage(f"Exhausted search - exiting")
                    return 
                extension, prepend = tuple
                new_transform = self.extendTransform(self.__last[0], extension, prepend)
                self.transforms.append(new_transform)

            self._setMessage(f"Trying transform {self.transforms[self._index]}")

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
            
            return [self.setupHeuristic(scores)]

        print("Heuristic DID NOT preload")