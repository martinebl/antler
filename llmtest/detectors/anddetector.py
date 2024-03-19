#!/usr/bin/env python3

from llmtest.detectors import Detector

class AndDetector(Detector):
    """
    Returns true if all given detectors do as well
    """
    def __init__(self, detectors: list[Detector]):
        self.detectors = detectors

    def detect(self, answer: str) -> bool:
        for detector in self.detectors:
            if not detector.detect(answer):
                return False
        return True