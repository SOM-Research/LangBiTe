from requests import Session
import json

# TODO: be able to select a particular model
# Hugging Chat models:
#   'meta-llama/Llama-2-70b-chat-hf'
#   'codellama/CodeLlama-34b-Instruct-hf'
#   'tiiuae/falcon-180B-chat'

class HuggingChatBroker:

    BASE_URL = "https://huggingface.co"
    HEADERS = {
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Host": "huggingface.co",
        "Origin": BASE_URL,
        "Sec-Fetch-Site": "same-origin",
        "Content-Type": "application/json",
        "Referer": BASE_URL + "/chat"
    }

    @property
    def cookiesdict(self):
        return self.session.cookies.get_dict()

    @property
    def cookies(self):
        return self._cookies
    
    @cookies.setter
    def cookies(self, value):
        self._cookies = { cookie["name"]: cookie["value"] for cookie in value }
    
    @property
    def session(self):
        if self._session is None:
            self._session = Session
        return self._session
    
    @session.setter
    def session(self, value) -> Session:
        self._session = value


    def __init__(self, cookie_path: str = "") -> None:
        cookies = dict
        with open(cookie_path, "r", encoding='utf-8') as f:
            cookies = json.load(f)
        self.cookies = cookies
        session = Session()
        session.cookies.update(self.cookies)
        session.get(self.BASE_URL + "/chat")
        self.session = session
        self.model = 'meta-llama/Llama-2-70b-chat-hf'
        self.conversation = self.new_conversation()

    
    def new_conversation(self) -> str:
        response = self.session.post(self.BASE_URL + "/chat/conversation", json={"model": self.model}, headers=self.HEADERS, cookies = self.cookiesdict)
        cid = json.loads(response.text)['conversationId']
        return cid
    

    def prompt(self, prompt: str) -> str:
        for response in self._stream_http_query(prompt):
            if response['type'] == "finalAnswer":
                result = response['text']            
        return result


    def _stream_http_query(self, text: str):

        request = {
            "inputs": text
        }
        headers = {
            "Origin": self.BASE_URL,
            "Referer": f"{self.BASE_URL}/chat/conversation/{self.conversation}",
            "Content-Type": "application/json"
        }

        last_response = {}
        last_response_met = False

        response = self.session.post(
            self.BASE_URL + f"/chat/conversation/{self.conversation}",
            json=request,
            stream=True,
            headers=headers,
            cookies=self.cookiesdict)
            
        for line in response.iter_lines(decode_unicode=True):
            if not line:
                continue

            obj = json.loads(line)
            type = obj['type']

            if type == "status":
                continue
            elif type == "stream":
                yield obj
            elif type == "finalAnswer":
                last_response = obj
                last_response_met = True
                break

            if last_response_met:
                break
        
        yield last_response
