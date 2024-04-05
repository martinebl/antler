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
        self.client = ollama.Client(options["host"] if "host" in options.keys() else "127.0.0.1:11434", timeout=30)

    def generate(self, prompt:str) -> str:
        response = self.client.generate(self.model, prompt)
        return response['response']

