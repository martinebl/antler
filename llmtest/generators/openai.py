#!/usr/bin/env python3
import openai
from dotenv import load_dotenv
import os
import backoff

from llmtest.generators import Generator

class OpenAI(Generator):
    # Load the environment file only on class definition and not on init
    load_dotenv()
    
    # Models
    # gpt-3.5-turbo
    # gpt-4-turbo-2024-04-09

    @staticmethod
    def needsApiKey() -> bool:
        return os.getenv("OPENAI_API_KEY") == None

    def __init__(self, model: str, api_key: str = None, options: dict = {}) -> None:
        super().__init__(model, api_key, options)


    @backoff.on_exception(
        backoff.fibo,
        (
            openai.RateLimitError,
            openai.InternalServerError,
            openai.APIError,
            openai.APITimeoutError,
            openai.APIConnectionError,
        ),
        max_tries=10,
    )
    @backoff.on_predicate(backoff.fibo, lambda ans: ans == None or len(ans) == 0, max_tries=10)
    def generate(self, prompt:str) -> str:
        client = openai.OpenAI(
            # Always use the given api key, and only the environment variable as backup
            api_key = os.getenv("OPENAI_API_TOKEN") if self.api_key == None else self.api_key
        )
        completion = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content