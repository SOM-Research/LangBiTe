from llm_abstract_factory import LLMFactory
from llm_huggingface_service import HuggingFaceChatService, HuggingFaceCompletionService

class HuggingFaceServiceBuilder:
    def __init__(self, model):
        self._instance = None
        self._model = model

    def __call__(self, huggingface_api_key, **_ignored):
        if not self._instance:
            self._instance = HuggingFaceCompletionService(huggingface_api_key, self._model)
        return self._instance

class HuggingFaceChatServiceBuilder:
    def __init__(self):
        self._instance = None
    
    def __call__(self, **_ignored):
        if not self._instance:
            self._instance = HuggingFaceChatService()
        return self._instance