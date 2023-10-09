import json
import requests
from huggingchat_broker import HuggingChatBroker
from llm_service import LLMService


class HuggingFaceService(LLMService):
    def __init__(self, huggingface_api_key, model):
        self._headers = {'Authorization': f'Bearer {huggingface_api_key}'}
        self._provider = 'HuggingFace'
        self._model = model

class HuggingFaceChatService(HuggingFaceService):
    def __init__(self, **ignored):
        self._provider = 'HuggingFace'
        self._model = 'HuggingChat'
    
    def execute_prompt(self, prompt):
        chatbot = HuggingChatBroker(cookie_path="resources/hugchat_cookies.json")
        try:
            response = chatbot.prompt(prompt)
        except:
            pass
        return response

class HuggingFaceCompletionService(HuggingFaceService):
    def execute_prompt(self, prompt):
        data = json.dumps(prompt)
        response = requests.request('POST', self._model, headers=self._headers, data=data)
        return json.loads(response.content.decode("utf-8"))[0]['generated_text']