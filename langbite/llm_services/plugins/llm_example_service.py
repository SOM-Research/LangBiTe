from langbite.llm_services.llm_service import LLMService
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Access the variable from the .env file

class ExampleService(LLMService):

    @property
    def api_client(self):
        return self.__api_client

    @property
    def promptSuffix(self):
        return self.__promptSuffix
    
    def __init__(self):
        # Using GPT-3.5 as an example for testing purposes, but it can be replaced with any other LLM.
        openai_api_key = os.getenv('API_KEY_OPENAI')
        self.__api_client = OpenAI(api_key=openai_api_key)
        self.provider = 'ExampleAICompany'
        self.model = 'gpt-3.5-turbo'
        self.__promptSuffix = ' Do not use carry returns in your response.'

    def execute_prompt(self, prompt):
        messages = [{ "role": "user", "content": prompt + self.promptSuffix }]
   
        completion = self.api_client.chat.completions.create(
            model = self.model,
            temperature = self.temperature,
            max_tokens = self.tokens,
            messages = messages)
        return completion.choices[0].message.content
