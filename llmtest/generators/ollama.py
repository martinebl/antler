#!/usr/bin/env python3
import ollama
import backoff

from llmtest.generators import Generator
class Ollama(Generator):
    """
    Use the locally running ollama instance. Will only work if the specified model
    is being served, on an active ollama instance.
    """
    def __init__(self, model: str, options: dict = {}) -> None:
        super().__init__(model, options)
        self.client = ollama.Client(options["host"] if "host" in options.keys() else "127.0.0.1:11434", timeout=30)

    @backoff.on_exception(backoff.fibo, TimeoutError, max_tries=10)
    @backoff.on_predicate(backoff.fibo, lambda ans: ans == None or len(ans) == 0, max_tries=10)
    def generate(self, prompt:str) -> str:
        response = self.client.generate(self.model, prompt)
        return response['response']

