import json
import requests
from huggingchat_broker import HuggingChatBroker
from llm_service import LLMService


class HuggingFaceService(LLMService):
    def __init__(self, huggingface_api_key, model):
        self.__headers = {'Authorization': f'Bearer {huggingface_api_key}'}
        self.provider = 'HuggingFace'
        self.model = model

class HuggingFaceChatService(HuggingFaceService):
    def __init__(self, **ignored):
        self.provider = 'HuggingFace'
        self.model = 'HuggingChat'
    
    def execute_prompt(self, prompt):
        chatbot = HuggingChatBroker(cookie_path="resources/hugchat_cookies.json", temperature=self.temperature, tokens=self.tokens)
        try:
            response = chatbot.prompt(prompt)
        except:
            pass
        return response

class HuggingFaceCompletionService(HuggingFaceService):
    def execute_prompt(self, prompt):
        data = json.dumps(prompt)
        response = requests.request('POST', self.model, headers=self.__headers, data=data)
        return json.loads(response.content.decode("utf-8"))[0]['generated_text']