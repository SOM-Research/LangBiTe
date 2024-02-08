from langbite.llm_services.llm_openai_service import OpenAIChatService

# class OpenAIServiceBuilder:
#     def __init__(self, model):
#         self._instance = None
#         self._model = model

#     def __call__(self, openai_api_key, **_ignored):
#         if not self._instance:
#             self._instance = OpenAICompletionService(openai_api_key, self._model)
#         return self._instance

class OpenAIChatServiceBuilder:
    def __init__(self, model):
        self._instance = None
        self._model = model
    
    def __call__(self, openai_api_key, **_ignored):
        if not self._instance:
            self._instance = OpenAIChatService(openai_api_key, self._model)
        return self._instance