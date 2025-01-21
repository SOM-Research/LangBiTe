import requests
from langbite.llm_services.llm_service import LLMService

class HuggingFaceConversationalServiceBuilder:
    def __init__(self, model):
        self._instance = None
        self._model = model

    def __call__(self, huggingface_api_key, **_ignored):
        if not self._instance:
            self._instance = HuggingFaceConversationalService(huggingface_api_key, self._model)
        return self._instance

class HuggingFaceService(LLMService):

    @property
    def headers(self):
        return self.__headers
    
    def __init__(self, huggingface_api_key, model):
        self.__headers = {'Authorization': f'Bearer {huggingface_api_key}'}
        self.provider = 'HuggingFace'
        self.model = model
    
    def query(self, payload):
        response = requests.post(self.model, headers=self.headers, json=payload)
        output = response.json()
        if 'error' in output: raise Exception('ERROR: ' + output['error'])
        return output

class HuggingFaceConversationalService(HuggingFaceService):
    def execute_prompt(self, prompt):
        payload = {"inputs": prompt, "parameters": {"return_full_text": False, "temperature": self.temperature, "max_new_tokens": self.tokens}}
        output = self.query(payload)
        return output[0]['generated_text']