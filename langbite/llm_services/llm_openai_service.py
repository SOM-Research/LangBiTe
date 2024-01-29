from langbite.llm_services.llm_service import LLMService
import openai


class OpenAIService(LLMService):

    @property
    def promptSuffix(self):
        return self.__promptSuffix
    
    def __init__(self, openai_api_key, model):
        openai.api_key = openai_api_key
        self.provider = 'OpenAI'
        self.model = model
        #self.__promptSuffix = ' Do not include any other text than the JSON object. Do not use carry returns in your response.'
        self.__promptSuffix = ' Do not use carry returns in your response.'


class OpenAIChatService(OpenAIService):
    #def __init__(self, openai_api_key):
    #    OpenAIService.__init__(self, openai_api_key, 'gpt-3.5-turbo')
    
    def execute_prompt(self, prompt):
        completion = openai.ChatCompletion.create(
            model = self.model,
            temperature = self.temperature,
            max_tokens = self.tokens,
            messages = [{"role": "user", "content": prompt + self.promptSuffix}])
        return completion.choices[0].message.content

class OpenAICompletionService(OpenAIService):
    def execute_prompt(self, prompt):
        completion = openai.Completion.create(
            model = self.model,
            temperature = self.temperature,
            max_tokens = self.tokens,
            prompt = prompt + self.promptSuffix)
        return completion.choices[0].text