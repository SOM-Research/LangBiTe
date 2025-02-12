from langbite.llm_services.llm_service import LLMService
from openai import OpenAI

class OpenAIChatServiceBuilder:
    def __init__(self, model):
        self._instance = None
        self._model = model
    
    def __call__(self, openai_api_key, **_ignored):
        if not self._instance:
            self._instance = OpenAIChatService(openai_api_key, self._model)
        return self._instance


class OpenAIService(LLMService):

    @property
    def api_client(self):
        return self.__api_client

    @property
    def promptSuffix(self):
        return self.__promptSuffix
    
    def __init__(self, openai_api_key, model):
        self.__api_client = OpenAI(api_key=openai_api_key)
        self.provider = 'OpenAI'
        self.model = model
        self.__promptSuffix = ' Do not use carry returns in your response.'


class OpenAIChatService(OpenAIService):
    def execute_prompt(self, prompt):
        messages = [{ "role": "user", "content": prompt + self.promptSuffix }]
        arguments = {"model": self.model, "messages": messages}
        if (self.temperature): arguments["temperature"] = self.temperature
        if (self.tokens): arguments["max_tokens"] = self.tokens
        completion = self.api_client.chat.completions.create(**arguments)
        return completion.choices[0].message.content