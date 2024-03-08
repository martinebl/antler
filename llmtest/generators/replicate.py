#!/usr/bin/env python3
import replicate
from dotenv import load_dotenv

from llmtest.generators import Generator

class Replicate(Generator):
    # Load the environment file only on class definition and not on init
    load_dotenv()

    def __init__(self, model: str, options: dict = {}) -> None:
        super().__init__(model, options)
        

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