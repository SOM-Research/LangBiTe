from ollama import Client
from langbite.llm_services.llm_service import LLMService

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
        output = ollama_client.generate(model=self.model, stream=False, prompt=prompt)
        return output['response']