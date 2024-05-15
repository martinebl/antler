#!/usr/bin/env python3
class Generator:
    """Base class for using LLMs to generate text"""

    @staticmethod
    def needsApiKey() -> bool:
        """
        This method should return true, only if the api needs an api key, 
        and it is not present as the correctly named environment variable
        """
        return False

    def __init__(self, model: str, api_key: str = None, options: dict = {}) -> None:
        self.model = model
        self.options = options
        self.api_key = api_key

    def generate(self, prompt: str) -> str:
        raise NotImplementedError("This method should be implemented in subclasses")

