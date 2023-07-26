import json
import requests
from huggingchat import HuggingChat
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
        chatbot = HuggingChat(cookie_path="resources/hugchat_cookies.json")
        id = chatbot.new_conversation()
        chatbot.change_conversation(id)
        response = chatbot.chat(prompt)#s[prompt[0]])
        return response

class HuggingFaceCompletionService(HuggingFaceService):
    def execute_prompt(self, prompt):
        data = json.dumps(prompt)
        response = requests.request('POST', self._model, headers=self._headers, data=data)
        return json.loads(response.content.decode("utf-8"))[0]['generated_text']