#!/usr/bin/env python3
from dotenv import load_dotenv
from octoai.core import ApiError
from octoai.text_gen import ChatMessage
import octoai.client
import os
import backoff

from antler.generators import Generator

class OctoAI(Generator):
    # Load the environment file only on class definition and not on init
    load_dotenv()
    
    # Models
    # gpt-3.5-turbo
    # gpt-3.5-turbo-0125
    # gpt-4-turbo-2024-04-09

    @staticmethod
    def needsApiKey() -> bool:
        return os.getenv("OCTOAI_TOKEN") == None

    def __init__(self, model: str, api_key: str = None, options: dict = {}) -> None:
        super().__init__(model, api_key, options)
        self.client = octoai.client.OctoAI(api_key=(api_key if api_key is not None else os.getenv("OCTOAI_TOKEN")))

    @backoff.on_exception(backoff.fibo, ApiError, max_tries=10)
    @backoff.on_predicate(backoff.fibo, lambda ans: ans == None or len(ans) == 0, max_tries=10)
    def generate(self, prompt: str) -> str:
        completion = self.client.text_gen.create_chat_completion(
            model=self.model,
            messages=[ChatMessage(
                role='user',
                content=prompt
            )],
            **self.options
        )
        return completion.choices[0].message.content