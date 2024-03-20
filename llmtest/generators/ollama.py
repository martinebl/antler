#!/usr/bin/env python3
import ollama
from llmtest.generators import Generator
class Ollama(Generator):
    """
    Use the locally running ollama instance. Will only work if the specified model
    is being served, on an active ollama instance.
    """
    def __init__(self, model: str, options: dict = {}) -> None:
        super().__init__(model, options)

    def generate(self, prompt:str) -> str:
        response = ollama.generate(self.model, prompt)
        return response['response']

