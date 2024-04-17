#!/usr/bin/env python3
import replicate
import os
from dotenv import load_dotenv
import backoff
import replicate.exceptions

from llmtest.generators import Generator

class Replicate(Generator):
    # Load the environment file only on class definition and not on init
    load_dotenv()

    # Models
    # mistralai/mixtral-8x7b-instruct-v0.1
    # mistralai/mistral-7b-v0.1
    # mistralai/mistral-7b-instruct-v0.2
    # meta/llama-2-70b-chat
    # meta/llama-2-7b-chat

    @staticmethod
    def needsApiKey() -> bool:
        return os.getenv("REPLICATE_API_TOKEN") == None


    def __init__(self, model: str, api_key: str = None, options: dict = {}) -> None:
        super().__init__(model, options)
        if api_key != None:
            os.environ["REPLICATE_API_TOKEN"] = api_key

        
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