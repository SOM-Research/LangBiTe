from langbite.utils import clean_string
import time

class PromptResponse:
    
    @property
    def instance(self) -> str:
        return self.__instance
    
    @property
    def response(self) -> str:
        return self.__response
    
    @response.setter
    def response(self, value: str):
        self.__response = clean_string(value)
    
    @property
    def execution_time(self):
        return self.__timestamp

    def __init__(self, instance, response):
        self.__instance = instance
        self.response = response
        self.__timestamp = time.localtime()