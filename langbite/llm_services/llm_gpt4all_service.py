from langbite.llm_services.llm_service import LLMService
from gpt4all import GPT4All

MODEL_NAME = "Phi-3-mini-4k-instruct.Q4_0.gguf"

class GPT4AllServiceBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self, **_ignored):
        if not self._instance:
            self._instance = GPT4AllService()
        return self._instance

class GPT4AllService(LLMService):

    def __init__(self):
        self.provider = 'GPT4All'
        self.llm = GPT4All(MODEL_NAME, device="cpu")

    def execute_prompt(self, prompt):
        with self.llm.chat_session():
            output = self.llm.generate(prompt)
            output = output.replace("<|assistant|>", "").replace('\n', ' ').strip()
            return output