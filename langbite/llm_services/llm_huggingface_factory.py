from langbite.llm_services.llm_huggingface_service import HuggingFaceCompletionService, HuggingFaceConversationalService, HuggingFaceQuestionAnsweringService

class HuggingFaceCompletionServiceBuilder:
    def __init__(self, model):
        self._instance = None
        self._model = model

    def __call__(self, huggingface_api_key, **_ignored):
        if not self._instance:
            self._instance = HuggingFaceCompletionService(huggingface_api_key, self._model)
        return self._instance

class HuggingFaceConversationalServiceBuilder:
    def __init__(self, model):
        self._instance = None
        self._model = model

    def __call__(self, huggingface_api_key, **_ignored):
        if not self._instance:
            self._instance = HuggingFaceConversationalService(huggingface_api_key, self._model)
        return self._instance

class HuggingFaceQuestionAnsweringServiceBuilder:
    def __init__(self, model):
        self._instance = None
        self._model = model

    def __call__(self, huggingface_api_key, **_ignored):
        if not self._instance:
            self._instance = HuggingFaceQuestionAnsweringService(huggingface_api_key, self._model)
        return self._instance