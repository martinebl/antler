#!/usr/bin/env python3
import llm
from generators.generator import Generator
class GPT4all(Generator):
    def __init__(self, model: str, options: dict = {}) -> None:
        super().__init__(model, options)

    def generate(self, prompt:str) -> str:
        #options are ignored for now
        model = llm.get_model(self.model)
        return model.prompt(prompt).text()

