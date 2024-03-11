#!/usr/bin/env python3
class Result:
    def __init__(self, name: str, attempt_scores: list[float]) -> None:
        self.name = name
        self.attempt_scores = attempt_scores
        self.score = sum(score[0] for score in self.attempt_scores) / len(self.attempt_scores)
        self.hit_count = sum(score[1] for score in self.attempt_scores)
        self.all_count = sum(score[2] for score in self.attempt_scores)

    def getName(self) -> str:
        return self.name

    def getAttemptScores(self) -> list[float]:
        return self.attempt_scores

    def getScore(self) -> float:
        return self.score
    
    def getHitCount(self) -> int:
        return self.hit_count
    
    def getAllCount(self) -> int:
        return self.all_count