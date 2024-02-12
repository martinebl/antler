#!/usr/bin/env python3
class Detector:
    """" A simple class, that detects certain target words in a text. Is paired up with a payload (clean prompt), to make a probe"""
    def __init__(self, targets: list[str],):
        self.targets = targets

    def detectTargets(self, answer: str) -> bool:
        for target in self.targets:
            if target in answer:
                return True
        return False