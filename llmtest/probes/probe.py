#!/usr/bin/env python3
from llmtest.detectors import Detector
class Probe:
    """Base class for Probe"""

    def __init__(self, payload:str, detectors: list[Detector]):
        self.payload = payload
        self.detectors = detectors

    def getPayload(self) -> str:
        return self.payload

    def runDetectors(self, answer: str) -> bool:
        for detector in self.detectors:
            if detector.detect(answer):
                return True
        return False