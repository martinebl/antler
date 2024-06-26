#!/usr/bin/env python3
from dotenv import load_dotenv
from openai import OpenAI
import os

from antler.generators import Generator

class Nvidia(Generator):
    # Load the environment file only on class definition and not on init
    load_dotenv()
    # model_uis = [
    #     "008cff6d-4f4c-4514-b61e-bcfad6ba52a7", # SMAUG 72B 
    #     "0e349b44-440a-44e1-93e9-abe8dcb27158", # LLama 2 70B 
    #     "1361fa56-61d7-4a12-af32-69a3825746fa", # Gemma 7b 
    #     "8f4118ba-60a8-4e6b-8574-e38a4067a4a3" # Mixtral 8x7B Instruct 
    # ]

    @staticmethod
    def needsApiKey() -> bool:
        return os.getenv("NVIDIA_API_TOKEN") == None

    def __init__(self, model: str, api_key: str = None, options: dict = {}) -> None:
        super().__init__(model, api_key, options)

    def generate(self, prompt: str) -> str:
        ans = ""
        # if (self.model not in Nvidia.model_uis):
        client = OpenAI(
            base_url = "https://integrate.api.nvidia.com/v1",
                        # Always use the given api key, and only the environment variable as backup
            api_key = os.getenv("NVIDIA_API_TOKEN") if self.api_key == None else self.api_key
        )

        completion = client.chat.completions.create(
            model=self.model,
            messages=[{"role":"user","content": prompt}],
            max_tokens=1024, # Max tokens is set really low in the API default, if it is not passed. Still costs a credit though
            temperature=0.5,
            top_p=1,
            **self.options, # If any of the keys above are present in this dictionairy, the passed options will overwrite the previous values
            stream=True
        )

        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                ans += chunk.choices[0].delta.content
        # else:
        #     # Old code. Kept if the new API goes down or something 
        #     invoke_url = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/functions/" + self.model

        #     headers = {
        #         "Authorization": "Bearer " + os.getenv("NVIDIA_API_TOKEN"),
        #         "accept": "text/event-stream",
        #         "content-type": "application/json",
        #     }

        #     payload = {
        #     "messages": [
        #         {
        #         "content": prompt,
        #         "role": "user"
        #         }
        #     ],
        #     "stream": True,
        #     **self.options
        #     }

        #     response = requests.post(invoke_url, headers=headers, json=payload, stream=True)

        #     for line in response.iter_lines():
        #         if line:
        #             decoded_line = line.decode("utf-8")[6:] # Remove the "data: " prefix from the response 
        #             try:
        #                 # Attempt to convert the JSON string to a Python dictionary
        #                 json_data = json.loads(decoded_line)

        #                 # Check if 'choices' and 'delta' keys exist to avoid KeyError
        #                 if 'choices' in json_data and json_data['choices']:
        #                     if 'delta' in json_data['choices'][0]:
        #                         delta = json_data['choices'][0]['delta']

        #                         # Extract the content
        #                         if 'content' in delta:
        #                             ans+= delta['content']
        #             except json.JSONDecodeError:
        #                 # Only happens on the final response, with the "[DONE]" tag, which is not valid json.
        #                 pass
        
        return ans
