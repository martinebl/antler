#!/usr/bin/env python3
from dotenv import load_dotenv
import requests
import os
import json

from llmtest.generators import Generator

class Nvidia(Generator):

    def __init__(self, model: str, options: dict = {}) -> None:
        super().__init__(model, options)
        load_dotenv()

    def generate(self, prompt: str) -> str:
        ans = ""

        # SMAUG 008cff6d-4f4c-4514-b61e-bcfad6ba52a7
        # LLama 2 70B 0e349b44-440a-44e1-93e9-abe8dcb27158
        invoke_url = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/functions/" + self.model

        headers = {
            "Authorization": "Bearer " + os.getenv("NVIDIA_API_TOKEN"),
            "accept": "text/event-stream",
            "content-type": "application/json",
        }

        payload = {
        "messages": [
            {
            "content": prompt,
            "role": "user"
            }
        ],
        "stream": True,
        **self.options
        }

        response = requests.post(invoke_url, headers=headers, json=payload, stream=True)

        for line in response.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")[6:] # Remove the "data: " prefix from the response 
                try:
                    # Attempt to convert the JSON string to a Python dictionary
                    json_data = json.loads(decoded_line)

                    # Check if 'choices' and 'delta' keys exist to avoid KeyError
                    if 'choices' in json_data and json_data['choices']:
                        if 'delta' in json_data['choices'][0]:
                            delta = json_data['choices'][0]['delta']

                            # Extract the content
                            if 'content' in delta:
                                ans+= delta['content']
                except json.JSONDecodeError:
                    # Only happens on the final response, with the "[DONE]" tag, which is not valid json.
                    pass
        
        return ans
