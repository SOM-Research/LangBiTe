import time
from llm_service import LLMService
import openai


class OpenAIService(LLMService):
    def __init__(self, openai_api_key, model):
        openai.api_key = openai_api_key
        self._provider = 'OpenAI'
        self._model = model
        self._promptSuffix = ' Do not include any other text than the JSON object. Do not use carry returns in your response.'

    # OpenAI trial license allows a request every 30 seconds
    def sleep(self):
        time.sleep(30)

class OpenAIChatService(OpenAIService):
    def __init__(self, openai_api_key):
        OpenAIService.__init__(self, openai_api_key, 'gpt-3.5-turbo')
    
    def execute_prompt(self, prompt):
        self.sleep()
        completion = openai.ChatCompletion.create(
            model = self._model,
            messages = [{"role": "user", "content": prompt + self._promptSuffix}])
        return completion.choices[0].message.content

class OpenAICompletionService(OpenAIService):
    def execute_prompt(self, prompt):
        self.sleep()
        completion = openai.Completion.create(
            model = self._model,
            max_tokens = 500,
            prompt = prompt + self._promptSuffix)
        return completion.choices[0].text