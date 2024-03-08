#!/usr/bin/env python3
class Result:
    def __init__(self, name: str, attempt_scores: list[float]) -> None:
        self.name = name
        self.attempt_scores = attempt_scores
        self.score = sum(self.attempt_scores) / len(self.attempt_scores)

    def getName(self) -> str:
        return self.name

    def getAttemptScores(self) -> list[float]:
        return self.attempt_scores

    def getScore(self) -> float:
        return self.score