#!/usr/bin/env python3
import llm
from antler.generators import Generator
class GPT4all(Generator):
    def __init__(self, model: str, api_key: str = None, options: dict = {}) -> None:
        super().__init__(model, api_key, options) # Api key is not used here

    def generate(self, prompt:str) -> str:
        #options are ignored for now
        model = llm.get_model(self.model)
        return model.prompt(prompt).text()

