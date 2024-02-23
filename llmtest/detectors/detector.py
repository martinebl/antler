#!/usr/bin/env python3
class Detector:
    """" The base class for detecting targets in a text. It should be paired up with a payload (clean prompt), to make a probe"""
    def __init__(self):
        pass

    def detect(self, answer: str) -> bool:
        raise NotImplementedError("This method should be implemented by subclasses")
        