#!/usr/bin/env python3
from antler.detectors import Detector

class SensitiveKeyWordDetector(Detector):
    """ A simple detector that looks for certain words in the answer, and returns true if a single one is present. Case sensitive"""
    def __init__(self, targets: list[str]) -> None:
        self.targets = targets

    def detect(self, answer: str) -> bool:
        for target in self.targets:
            if target in answer:
                return True
        return False