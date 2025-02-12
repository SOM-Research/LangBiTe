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
        #adopted_prompt = prompt + ' Be brief and concise, and do not use more than 20 words in your response.'# [{"role": "user", "content": prompt + ' Be brief and concise, and do not use more than 20 words in your response.'}]
        adopted_prompt = [{"role": "user", "content": prompt}]
        options =  {"temperature": self.temperature, "num_predict": self.tokens}
        output = ollama_client.chat(model=self.model, stream=False, messages=adopted_prompt, options=options)
        #output = ollama_client.generate(model=self.model, stream=False, prompt=prompt, options=options)
        #return output['response']
        return output.message.content