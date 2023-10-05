from requests import Session
import requests
import json
import os
import uuid
import logging
import typing
import traceback
from typing import Union


class ModelOverloadedError(Exception):
    """
    HF Model Overloaded Error
    
    Raised when hf return response `{"error":"Model is overloaded","error_type":"overloaded"}`
    """
    pass


class ChatBotInitError(Exception):
    """
    ChatBot Init Error
    
    Raised when chatbot init failed
    """
    pass


class CreateConversationError(Exception):
    """
    Create Conversation Error
    
    Raised when create conversation failed
    """
    pass


class InvalidConversationIDError(Exception):
    """
    Invalid Conversation ID Error
    
    Raised when using a invalid conversation id
    """
    pass


class DeleteConversationError(Exception):
    """
    Delete Conversation Error
    
    Raised when delete conversation failed
    """
    pass


class ChatError(Exception):
    """
    Chat Error
    
    Raised when chat failed
    """
    pass

class WebSearchSource:
    title: str
    link: str
    hostname: str

class QueryResult:
    """
    The result of a non-stream query.
    """
    text: str
    web_search: bool
    web_search_sources: list[WebSearchSource]

    def __str__(self) -> str:
        return self.text

    def __add__(self, other: str) -> str:
        return self.text + other
    
    def __radd__(self, other: str) -> str:
        return other + self.text
    
    def __iadd__(self, other: str) -> str:
        self.text += other
        return self.text

    def __getitem__(self, key: str) -> str:
        if key == "text":
            return self.text
        elif key == "web_search":
            return self.web_search
        elif key == "web_search_sources":
            return self.web_search_sources


class HuggingChat:
    
    cookies: dict
    """Cookies for authentication"""

    session: Session
    """HuggingChat session"""

    def __init__(
        self,
        cookies: dict = None,
        cookie_path: str = "",
        default_llm: Union[int, str] = 0,
    ) -> None:
        """
        default_llm: 
        0: `meta-llama/Llama-2-70b-chat-hf`
        1: `OpenAssistant/oasst-sft-6-llama-30b-xor`
        2: `codellama/CodeLlama-34b-Instruct-hf`
        3: `tiiuae/falcon-180B-chat`
        """
        if cookies is None and cookie_path == "":
            raise ChatBotInitError("Authentication is required now, but no cookies provided. See tutorial at https://github.com/Soulter/hugging-chat-api")
        elif cookies is not None and cookie_path != "":
            raise ChatBotInitError("Both cookies and cookie_path provided")
        
        if cookies is None and cookie_path != "":
            # read cookies from path
            if not os.path.exists(cookie_path):
                raise ChatBotInitError(f"Cookie file {cookie_path} not found. Note: The file must be in JSON format and must contain a list of cookies. See more at https://github.com/Soulter/hugging-chat-api")
            with open(cookie_path, "r", encoding='utf-8') as f:
                cookies = json.load(f)

        # convert cookies to KV format
        if isinstance(cookies, list):
            cookies = {cookie["name"]: cookie["value"] for cookie in cookies}

        self.cookies = cookies

        self.hf_base_url = "https://huggingface.co"
        self.json_header = {"Content-Type": "application/json"}
        self.session = self.get_hc_session()
        self.conversation_id_list = []
        self.__not_summarize_cids = []
        self.accepted_welcome_modal = False # It is no longer required to accept the welcome modal
        self.llms = [
                'meta-llama/Llama-2-70b-chat-hf',
                'codellama/CodeLlama-34b-Instruct-hf', 
                'tiiuae/falcon-180B-chat'
        ] # The array is up to date as of October 2, 2023
        self.active_model = self.llms[default_llm]
        self.current_conversation = self.new_conversation()
        self.system_prompts = {}

    def get_hc_session(self) -> Session:
        session = Session()
        # set cookies
        session.cookies.update(self.cookies)
        session.get(self.hf_base_url + "/chat")
        return session
    
    def get_headers(self, ref=True, ref_cid = None) -> dict:
        _h = {
            "Accept": "*/*",
            "Connection": "keep-alive",
            "Host": "huggingface.co",
            "Origin": "https://huggingface.co",
            "Sec-Fetch-Site": "same-origin",
            "Content-Type": "application/json",
            "Sec-Ch-Ua-Platform": "Windows",
            "Sec-Ch-Ua": "Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Microsoft Edge\";v=\"116",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        }
        if ref:
            if ref_cid is None:
                ref_cid = self.current_conversation
            _h["Referer"] = f"https://huggingface.co/chat/conversation/{ref_cid}"
        return _h
    
    def get_cookies(self) -> dict:
        return self.session.cookies.get_dict()
    

    # # NOTE: To create a copy when calling this, call it inside of list().
    # #       If not, when updating or altering the values in the variable will
    # #       also be applied to this class's variable.
    # #       This behavior is with any function returning self.<var_name>. It
    # #       acts as a pointer to the data in the object.
    # #
    # # Returns a pointer to this objects list that contains id of conversations.
    # def get_conversation_list(self) -> list:
    #     return list(self.conversation_id_list)
    
    # def get_active_llm_index(self) -> int:
    #     return self.llms.index(self.active_model)
    
    # def accept_ethics_modal(self):
    #     '''
    #     [Deprecated Method]
    #     '''
    #     response = self.session.post(self.hf_base_url + "/chat/settings", headers=self.get_headers(ref=False), cookies=self.get_cookies(), allow_redirects=True, data={
    #         "ethicsModalAccepted": "true",
    #         "shareConversationsWithModelAuthors": "true",
    #         "ethicsModalAcceptedAt": "",
    #         "activeModel": str(self.active_model)
    #     })

    #     if response.status_code != 200:
    #         raise Exception(f"Failed to accept ethics modal with status code: {response.status_code}. {response.content.decode()}")
        
    #     return True
    
    def new_conversation(self) -> str:
        '''
        Create a new conversation. Return the new conversation id. You should change the conversation by calling change_conversation() after calling this method.
        '''
        err_count = 0

        # Accept the welcome modal when init.
        # 17/5/2023: This is not required anymore.
        # if not self.accepted_welcome_modal:
        #     self.accept_ethics_modal()

        # Create new conversation and get a conversation id.

        _header = self.get_headers(ref = False)
        _header['Referer'] = "https://huggingface.co/chat"

        resp = ""
        while True:
            try:
                resp = self.session.post(self.hf_base_url + "/chat/conversation", json={"model": self.active_model}, headers=_header, cookies = self.get_cookies())
                logging.debug(resp.text)
                cid = json.loads(resp.text)['conversationId']
                self.conversation_id_list.append(cid)
                self.__not_summarize_cids.append(cid) # For the 1st chat, the conversation needs to be summarized.
                self.__preserve_context(cid = cid, ending = "1_1")
                return cid
            
            except BaseException as e:
                err_count += 1
                logging.debug(f" Failed to create new conversation. Retrying... ({err_count})")
                if err_count > 5:
                    raise CreateConversationError(f"Failed to create new conversation with status code: {resp.status_code}. ({err_count})")
                continue
    
    # def change_conversation(self, conversation_id: str) -> bool:
    #     '''
    #     Change the current conversation to another one. Need a valid conversation id.
    #     '''
    #     if conversation_id not in self.conversation_id_list:
    #         raise InvalidConversationIDError("Invalid conversation id, not in conversation list.")
    #     self.current_conversation = conversation_id
    #     return True
    
    # def get_available_llm_models(self) -> list:
    #     '''
    #     Get all available models that exists in huggingface.co/chat.
    #     Returns a hard-code array.
    #     '''
    #     return self.llms

    # def set_system_prompt(self, prompt: str, llmIndex: int = None):
    #     '''
    #     Sets a system prompt for the given model index
    #     You need to create a new conversation for this to work
    #     '''

    #     if llmIndex is None:
    #         llmIndex = self.get_active_llm_index()

    #     elif llmIndex > len(self.llms)-1 or llmIndex < 0:
    #         raise IndexError("Out of range of llm index")
        
    #     self.system_prompts[self.llms[llmIndex]] = prompt

    #     settings = {
    #         "customPrompts": ("", json.dumps(self.system_prompts))
    #     }

    #     self.session.post(self.hf_base_url + "/chat/settings", headers={ "Referer": "https://huggingface.co/chat" }, cookies=self.get_cookies(), allow_redirects=True, files=settings)

    # def check_operation(self) -> bool:
    #     r = self.session.post(self.hf_base_url + f"/chat/conversation/{self.current_conversation}/__data.json?x-sveltekit-invalidated=1_1", headers=self.get_headers(ref=True), cookies=self.get_cookies())
    #     return r.status_code == 200

    def _stream_query(
        self,
        text: str,
        web_search: bool=False,
        temperature: float=0.1,
        top_p: float=0.95,
        repetition_penalty: float=1.2,
        top_k: int=50,
        truncate: int=1000,
        watermark: bool=False,
        max_new_tokens: int=1024,
        stop: list=["</s>"],
        return_full_text: bool=False,
        use_cache: bool=False,
        is_retry: bool=False,
        retry_count: int=5,
        _stream_yield_all: bool=False, # yield all responses from the server.
    ) -> typing.Generator[dict, None, None]:
        
        if retry_count <= 0:
            raise Exception("the parameter retry_count must be greater than 0.")
        if self.current_conversation == "":
            self.current_conversation = self.new_conversation()
        if text == "":
            raise Exception("the prompt can not be empty.")

        req_json = {
            "inputs": text,
            "parameters": {
                "temperature": temperature,
                "top_p": top_p,
                "repetition_penalty": repetition_penalty,
                "top_k": top_k,
                "truncate": truncate,
                "watermark": watermark,
                "max_new_tokens": max_new_tokens,
                "stop": stop,
                "return_full_text": return_full_text,
                "stream": True,
            },
            "options": {
                    "use_cache": use_cache,
                    "is_retry": is_retry,
                    "id": str(uuid.uuid4()),
            },
            "stream": True,
            "web_search": web_search,
        }
        headers = {
            "Origin": "https://huggingface.co",
            "Referer": f"https://huggingface.co/chat/conversation/{self.current_conversation}",
            "Content-Type": "application/json",
            "Sec-ch-ua": '"Chromium";v="94", "Microsoft Edge";v="94", ";Not A Brand";v="99"',
            "Sec-ch-ua-mobile": "?0",
            "Sec-ch-ua-platform": '"Windows"',
            "Accept": "*/*",
            "Accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        }
        last_obj = {}
        
        break_label = False

        while retry_count > 0:
            resp = self.session.post(self.hf_base_url + f"/chat/conversation/{self.current_conversation}", json=req_json, stream=True, headers=headers, cookies=self.session.cookies.get_dict())

            if resp.status_code != 200:
                retry_count -= 1
                if retry_count <= 0:
                    raise ChatError(f"Failed to chat. ({resp.status_code})")
            
            try:
                for line in resp.iter_lines(decode_unicode=True):
                    if not line:
                        continue
                    res = line
                    obj = json.loads(res)
                    _type = obj['type']

                    if _stream_yield_all:
                        if _type == "finalAnswer":
                            last_obj = obj
                            break_label = True
                            break
                        yield obj
                    else:
                        if _type == "status":
                            continue
                        elif _type == "stream":
                            yield obj
                        elif _type == "finalAnswer":
                            last_obj = obj
                            break_label = True
                            break
                        elif _type == "webSearch":
                            continue
                        elif "error" in obj:
                            raise ChatError(obj["error"])
                        else:
                            raise ChatError(obj)
            except requests.exceptions.ChunkedEncodingError:
                pass
            except BaseException as e:
                traceback.print_exc()
                if "Model is overloaded" in str(e):
                    raise ModelOverloadedError("Model is overloaded, please try again later or switch to another model.")
                raise ChatError(f"Failed to parse response: {res}")
            if break_label:
                break
        
        try:
            # if self.current_conversation in self.__not_summarize_cids:
            #     self.summarize_conversation()
            #     self.__not_summarize_cids.remove(self.current_conversation)
            self.__preserve_context(ref_cid = self.current_conversation)
        except:
            pass
        
        yield last_obj

    # def _stream_query_filter(
    #     self,
    #     *args,
    #     **kwargs,
    # ) -> typing.Generator[dict, None, None]:
    #     for resp in self._stream_query(*args, **kwargs):
    #         if '_stream_yield_all' in kwargs and kwargs['_stream_yield_all']:
    #             # If _stream_yield_all is True, yield all responses from the server.
    #             yield resp
    #         else:
    #             if resp['type'] == "stream":
    #                 yield resp

    def _non_stream_query(
        self,
        text: str,
        web_search: bool=False,
        temperature: float=0.1,
        top_p: float=0.95,
        repetition_penalty: float=1.2,
        top_k: int=50,
        truncate: int=1000,
        watermark: bool=False,
        max_new_tokens: int=1024,
        stop: list=["</s>"],
        return_full_text: bool=False,
        use_cache: bool=False,
        is_retry: bool=False,
        retry_count: int=5,
    ) -> QueryResult:
        query_result = QueryResult()
        ws = []
        sources = []
        for resp in self._stream_query(
            text,
            web_search,
            temperature,
            top_p,
            repetition_penalty,
            top_k,
            truncate,
            watermark,
            max_new_tokens,
            stop,
            return_full_text,
            use_cache,
            is_retry,
            retry_count,
            _stream_yield_all=True,
        ): 
            if resp['type'] == "webSearch" and "messageType" in resp and resp["messageType"] == "sources":
                sources = resp['sources']

            if resp['type'] == "finalAnswer":
                query_result.text = resp['text']
                query_result.web_search = web_search
                query_result.web_search_sources = ws
                for source in sources:
                    wss = WebSearchSource()
                    wss.title = source['title']
                    wss.link = source['link']
                    wss.hostname = source['hostname']
                    ws.append(wss)
            
        return query_result
    
    def query(
        self,
        text: str,
        web_search: bool=False,
        temperature: float=0.1,
        top_p: float=0.95,
        repetition_penalty: float=1.2,
        top_k: int=50,
        truncate: int=1000,
        watermark: bool=False,
        max_new_tokens: int=1024,
        stop: list=["</s>"],
        return_full_text: bool=False,
        stream: bool=False,
        _stream_yield_all: bool=False, # For stream mode, yield all responses from the server.
        use_cache: bool=False,
        is_retry: bool=False,
        retry_count: int=5,
    ) -> typing.Union[typing.Generator[dict, None, None], QueryResult]:

        """
        Send a message to the current conversation. Return the response text.
        You can customize these optional parameters.
        You can turn on the web search by set the parameter `web_search` to True
        When the `stream` is True, it will return a generator that yields the response from the server.
        When the `stream` is False, it will return a QueryResult object.

        About the QueryResult object:
        - `text`: The response text.
        - `web_search`: Whether the response contains web search results.
        - `web_search_sources`: The web search results. It is a list of WebSearchSource objects.

        You can:
        - query_result.text
        - query_result["text"]
        - query_result.text + "a string"
        - query_result.text += "a string"
        - ...
        """

        if stream:
            return self._stream_query_filter(
                text,
                web_search,
                temperature,
                top_p,
                repetition_penalty,
                top_k,
                truncate,
                watermark,
                max_new_tokens,
                stop,
                return_full_text,
                use_cache,
                is_retry,
                retry_count,
                _stream_yield_all = _stream_yield_all,
            )
        else:
            return self._non_stream_query(
                text,
                web_search,
                temperature,
                top_p,
                repetition_penalty,
                top_k,
                truncate,
                watermark,
                max_new_tokens,
                stop,
                return_full_text,
                use_cache,
                is_retry,
                retry_count,
            )

    def chat(
        self,
        text: str,
        web_search: bool=False,
        temperature: float=0.1,
        top_p: float=0.95,
        repetition_penalty: float=1.2,
        top_k: int=50,
        truncate: int=1000,
        watermark: bool=False,
        max_new_tokens: int=1024,
        stop: list=["</s>"],
        return_full_text: bool=False,
        stream: bool=False,  # make no sense
        use_cache: bool=False,
        is_retry: bool=False,
        retry_count: int=5,
    ) -> QueryResult:
        '''
        Send a message to the current conversation. Return the response text.
        You can customize these optional parameters.
        You can turn on the web search by set the parameter `web_search` to True

        If you want to stream the response, use the `query` method instead and set it `stream` parameter to `True`.

        About the QueryResult object:
        - `text`: The response text.
        - `web_search`: Whether the response contains web search results.
        - `web_search_sources`: The web search results. It is a list of WebSearchSource objects.

        You can:
        - query_result.text
        - query_result["text"]
        - query_result.text + "a string"
        - query_result.text += "a string"
        - ...
        '''

        return self.query(
            text,
            web_search,
            temperature,
            top_p,
            repetition_penalty,
            top_k,
            truncate,
            watermark,
            max_new_tokens,
            stop,
            return_full_text,
            False,
            use_cache,
            is_retry,
            retry_count,
        )

    def __preserve_context(self, cid: str = None, ending: str = "1_", ref_cid: str = "") -> bool:
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
            'Accept': "*/*",
        }
        if ref_cid == "":
            headers["Referer"] = "https://huggingface.co/chat"
        else:
            headers["Referer"] = f"https://huggingface.co/chat/conversation/{ref_cid}"
        # print(headers)
        cookie = {
            'hf-chat': self.get_cookies()['hf-chat'],
        }
        if cid is None:
            cid = self.current_conversation
        url = f"https://huggingface.co/chat/conversation/{cid}/__data.json?x-sveltekit-invalidated={ending}"
        response = self.session.get(url, cookies = cookie, headers = headers, data = {})
        return response.status_code == 200