#!/usr/bin/env python3
from llmtest.transformers import Transformer

class Result:
    def __init__(self, payload: str, applied_transforms: list[(Transformer, bool)]) -> None:
        self.payload = payload
        self.applied_transforms = applied_transforms

