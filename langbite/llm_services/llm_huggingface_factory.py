import requests
from langbite.llm_services.llm_service import LLMService

class HuggingFaceConversationalServiceBuilder:
    def __init__(self, model, inference_api_url):
        self._instance = None
        self._model = model
        self._inference_api_url = inference_api_url

    def __call__(self, huggingface_api_key, **_ignored):
        if not self._instance:
            self._instance = HuggingFaceConversationalService(huggingface_api_key, self._model, self._inference_api_url)
        return self._instance

class HuggingFaceService(LLMService):

    @property
    def headers(self):
        return self.__headers
    
    def __init__(self, huggingface_api_key, model, inference_api_url):
        self.__headers = {'Authorization': f'Bearer {huggingface_api_key}'}
        self.provider = 'HuggingFace'
        self.model = model
        self.__api_url = inference_api_url
    
    def query(self, payload):
        response = requests.post(self.__api_url, headers=self.headers, json=payload)
        output = response.json()
        if 'error' in output: raise Exception('ERROR: ' + output['error'])
        return output

class HuggingFaceConversationalService(HuggingFaceService):
    def execute_prompt(self, prompt):
        payload = {"inputs": prompt, "parameters": {"return_full_text": False, "temperature": self.temperature, "max_new_tokens": self.tokens}}
        output = self.query(payload)
        return output[0]['generated_text']