#!/usr/bin/env python3
import replicate
from dotenv import load_dotenv
import backoff
import replicate.exceptions

from llmtest.generators import Generator

class Replicate(Generator):
    # Load the environment file only on class definition and not on init
    load_dotenv()

    def __init__(self, model: str, options: dict = {}) -> None:
        super().__init__(model, options)
        
    @backoff.on_exception(backoff.fibo, replicate.exceptions.ReplicateError, max_tries=10)
    @backoff.on_predicate(backoff.fibo, lambda ans: ans == None or len(ans) == 0, max_tries=10)
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