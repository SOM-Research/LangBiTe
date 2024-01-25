import json
import requests
from langbite.llm_service import LLMService


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
        #return json.loads(response.content.decode("utf-8"))[0]['generated_text'] <- old GPT2 ones
        if 'error' in output: raise Exception('ERROR: ' + output['error'])
        return output

class HuggingFaceCompletionService(HuggingFaceService):
    def execute_prompt(self, prompt):
        payload = {"inputs": prompt, "parameters": {"return_full_text": False, "temperature": self.temperature}}
        output = self.query(payload)
        if 'error' in output: raise Exception('ERROR: ' + output['error'])
        return output[0]['generated_text']

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