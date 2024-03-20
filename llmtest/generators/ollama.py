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
        self.use_custom_client = False
        if "host" in options.keys():
            self.use_custom_client = True
            self.client = ollama.Client(host=options["host"])

    def generate(self, prompt:str) -> str:
        if self.use_custom_client:
            response = self.client.generate(self.model, prompt)
        else:
            response = ollama.generate(self.model, prompt)
        return response['response']

