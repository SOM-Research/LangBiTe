import os

import replicate
from langbite.llm_services.llm_service import LLMService


class ReplicateService(LLMService):

    def __init__(self, replicate_api_key, model):
        self.provider = 'Replicate'
        self.model = model
        os.environ['REPLICATE_API_TOKEN'] = replicate_api_key

    def execute_prompt(self, prompt):
        answer = replicate.run(
            self.model,
            input={
                "debug": False,
                "system_prompt": "",
                "prompt": prompt,
                "temperature": self.temperature,
                "max_new_tokens": self.tokens,
                # "top_k": 50,
                # "top_p": 1,
                # "min_new_tokens": -1
            },
        )
        return ''.join(answer)
