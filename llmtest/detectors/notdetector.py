#!/usr/bin/env python3

from llmtest.detectors import Detector

class NotDetector(Detector):
    """
    Returns the negated truth value of the given detector
    """
    def __init__(self, detector: Detector):
        self.detector = detector

    def detect(self, answer: str) -> bool:
        return not self.detector.detect(answer)