#!/usr/bin/env python3
from llmtest.transforms import Transform
from llmtest.probes import Probe

class Result:
    def __init__(self, transform: Transform, hits: int, probes: list[Probe]) -> None:
        self.transform = transform
        self.hits = hits
        self.probes = probes
        self.score = hits/len(probes) if len(probes) > 0 else 0