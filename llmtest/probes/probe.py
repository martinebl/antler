#!/usr/bin/env python3
import json
from llmtest.detectors import Detector
class Probe:
    """Base class for Probe"""

    def __init__(self, payload:str, detector: Detector):
        self.payload = payload
        self.detector = detector

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Probe):
            return self.__dict__ == other.__dict__

    def getPayload(self) -> str:
        return self.payload

    def runDetector(self, answer: str) -> bool:
        return self.detector.detect(answer)