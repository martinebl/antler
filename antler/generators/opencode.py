#!/usr/bin/env python3
import openai
from dotenv import load_dotenv
import os
import backoff

from antler.generators import Generator

class OpenCode(Generator):
    # Load the environment file only on class definition and not on init
    load_dotenv()

    BASE_URL = "https://opencode.ai/zen/go/v1"

    # Models
    # qwen3.6-plus
    # qwen3.8-max
    # minimax-m3

    @staticmethod
    def needsApiKey() -> bool:
        return os.getenv("OPENCODE_API_TOKEN") == None

    def __init__(self, model: str, api_key: str = None, options: dict = {}) -> None:
        super().__init__(model, api_key, options)
        self.client = openai.OpenAI(
            base_url=OpenCode.BASE_URL,
            # Always use the given api key, and only the environment variable as backup
            api_key=(api_key if api_key is not None else os.getenv("OPENCODE_API_TOKEN")),
        )

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
    def generate(self, prompt: str) -> str:
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            **self.options
        )
        return completion.choices[0].message.content
