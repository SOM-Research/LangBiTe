import json
import requests
from llm_service import LLMService


class HuggingFaceService(LLMService):

    @property
    def headers(self):
        return self.__headers
    
    def __init__(self, huggingface_api_key, model):
        self.__headers = {'Authorization': f'Bearer {huggingface_api_key}'}
        self.provider = 'HuggingFace'
        self.model = model
    
    def query(self, payload):
        data = json.dumps(payload)
        response = requests.request('POST', self.model, headers=self.headers, data=data)
        output = response.json()
        #return json.loads(response.content.decode("utf-8"))[0]['generated_text'] <- old GPT2 ones
        if 'error' in output: raise Exception('ERROR: ' + output['error'])
        return output

class HuggingFaceCompletionService(HuggingFaceService):
    def execute_prompt(self, prompt):
        output = self.query(prompt)
        #data = json.dumps(prompt)
        #response = requests.request('POST', self.model, headers=self.headers, data=data)
        #output = response.json()
        #return json.loads(response.content.decode("utf-8"))[0]['generated_text'] <- old GPT2 ones
        if 'error' in output: raise Exception('ERROR: ' + output['error'])
        return output['generated_text']

class HuggingFaceQuestionAnsweringService(HuggingFaceService):

    __context = 'The question provided is about the current sociological context.'

    def execute_prompt(self, prompt):
        data = { 'inputs': {
                'question': prompt,
                'context': self.__context
            }
        }
        output = self.query(data)
        #data = json.dumps(data)
        #response = requests.request('POST', self.model, headers=self.headers, data=data)
        #output = response.json()
        if 'error' in output: raise Exception('ERROR: ' + output['error'])
        return output['answer']