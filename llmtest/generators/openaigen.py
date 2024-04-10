#!/usr/bin/env python3
from openai import OpenAI
from dotenv import load_dotenv
import os

from llmtest.generators import Generator

class OpenAIGen(Generator):
    load_dotenv()
    # model: gpt-3.5-turbo
    
    def __init__(self, model: str, options: dict = {}) -> None:
        super().__init__(model, options)


    def generate(self, prompt:str) -> str:
        client = OpenAI(
            api_key = os.getenv("OPENAI_API_TOKEN")
        )
        completion = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content