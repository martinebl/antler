#!/usr/bin/env python3
import re

from antler.detectors import Detector

class RegexDetector(Detector):

    def __init__(self, patterns: list[str]):
        self.regexes = [re.compile(pattern) for pattern in patterns]

    def detect(self, answer: str) -> bool:
        for regex in self.regexes:
            if regex.search(answer):
                return True
        return False