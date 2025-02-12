from abc import abstractmethod


class LLMService:
    @abstractmethod
    def execute_prompt(self, prompt):
        pass

    @property
    def provider(self):
        return self.__provider

    @provider.setter
    def provider(self, value):
        self.__provider = value

    @property
    def model(self):
        return self.__model
    
    @model.setter
    def model(self, value):
        self.__model = value

    @property
    def temperature(self):
        if hasattr(self, '__temperature'): return self.__temperature
        else: return None
    
    @temperature.setter
    def temperature(self, value):
        self.__temperature = value

    @property
    def tokens(self):
        if hasattr(self, '__tokens'): return self.__tokens
        else: return None
    
    @tokens.setter
    def tokens(self, value):
        self.__tokens = value