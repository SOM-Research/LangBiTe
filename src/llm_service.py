from abc import abstractmethod


class LLMService:
    @abstractmethod
    def execute_prompt(self, prompt):
        pass

    @property
    def provider(self):
        return self._provider

    @property
    def model(self):
        return self._model