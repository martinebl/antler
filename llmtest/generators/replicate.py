#!/usr/bin/env python3
import replicate
from dotenv import load_dotenv

from llmtest.generators import Generator

class Replicate(Generator):
    def __init__(self, model: str, options: dict = {}) -> None:
        super().__init__(model, options)
        load_dotenv()
        

    def generate(self, prompt: str) -> str:
        ans = ""

        for event in replicate.stream(
            self.model,
            input={
                "prompt": prompt,
                **self.options
            }):
            ans+=str(event)
        
        return ans