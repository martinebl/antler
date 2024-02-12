#!/usr/bin/env python3
class Generator:
    """Base class for using LLMs to generate text"""

    def __init__(self, model: str, options: dict = {}) -> None:
        self.model = model
        self.options = options

    def generate(self, prompt: str) -> str:
        raise NotImplementedError("This method should be implemented in subclasses")

