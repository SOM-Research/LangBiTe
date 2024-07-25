import requests
from langbite.llm_services.llm_service import LLMService


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

class HuggingFaceCompletionService(HuggingFaceService):
    def execute_prompt(self, prompt):
        payload = {"inputs": prompt} #, "parameters": {"return_full_text": False, "temperature": self.temperature}}
        output = self.query(payload)
        return output[0]['generated_text']

class HuggingFaceConversationalService(HuggingFaceService):
    def execute_prompt(self, prompt):
        payload = {"inputs": prompt, "parameters": {"return_full_text": False, "temperature": self.temperature, "max_new_tokens": self.tokens}}
        output = self.query(payload)
        return output[0]['generated_text']

# TODO: to properly develop an integration with HF's question answering models
class HuggingFaceQuestionAnsweringService(HuggingFaceService):

    __context = 'The question provided is about the current sociological context.'

    def execute_prompt(self, prompt):
        data = { 'inputs': {
                'question': prompt,
                'context': self.__context
            }
        }
        output = self.query(data)
        if 'error' in output: raise Exception('ERROR: ' + output['error'])
        return output['answer']