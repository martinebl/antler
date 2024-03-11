#!/usr/bin/env python3
from llmtest.detectors import Detector

class SimpleDetector(Detector):
    """ A simple detector that looks for certain words in the answer, and returns true if a single one is present """
    def __init__(self, targets: list[str]) -> None:
        self.targets = targets

    def detect(self, answer: str) -> bool:
        low_ans = answer.lower()
        for target in self.targets:
            if target.lower() in low_ans:
                return True
        return False