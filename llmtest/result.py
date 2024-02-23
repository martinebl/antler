#!/usr/bin/env python3
from llmtest.transforms import Transform

class Result:
    def __init__(self, payload: str, applied_transforms: list[(Transform, bool)]) -> None:
        self.payload = payload
        self.applied_transforms = applied_transforms

