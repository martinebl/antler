#!/usr/bin/env python3

from llmtest.detectors import Detector

class OrDetector(Detector):
    """
    Returns true if a single of the given detectors do
    """
    def __init__(self, detectors: list[Detector]):
        self.detectors = detectors

    def detect(self, answer: str) -> bool:
        for detector in self.detectors:
            if detector.detect(answer):
                return True
        return False