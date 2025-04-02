from ollama import Client
from langbite.llm_services.llm_service import LLMService
import re

class OLlamaServiceBuilder:
    def __init__(self, model):
        self.__instance = None
        self.__model = model

    def __call__(self, ollama_url, **_ignored):
        if not self.__instance:
            self.__instance = OLlamaService(self.__model, ollama_url)
        return self.__instance

class OLlamaService(LLMService):

    def __init__(self, model, ollama_url):
        self.provider = 'OLlama'
        self.model = model
        self.__url = ollama_url

    def execute_prompt(self, prompt):
        ollama_client = Client(host=self.__url)
        adopted_prompt = [{"role": "user", "content": prompt}]
        options =  {"temperature": self.temperature, "num_predict": self.tokens}
        output = ollama_client.chat(model=self.model, stream=False, messages=adopted_prompt, options=options)
        # the following is to remove the thinking from DeepSeek models
        actual_response = re.sub(r"<think>.*?</think>", "", output.message.content, flags=re.DOTALL).strip()
        return actual_response