from test_scenario import TestScenario
from prompt import Prompt
import llm_factory
from llm_service import LLMService
from dotenv import load_dotenv
import os
from view_model import EvaluationView, ResponseView
import time

class TestExecution:

    @property
    def responses(self) -> list[ResponseView]:
        if self.__responses is None: self.__responses = []
        return self.__responses

    @property
    def evaluations(self) -> list[EvaluationView]:
        if self.__evaluations is None: self.__evaluations = []
        return self.__evaluations
    
    def __init__(self, scenario: TestScenario):
        self.__scenario = scenario
        self.__responses = []
        self.__evaluations = []
        load_dotenv()
        self.__config = {
            'openai_api_key' : os.environ["API_KEY_OPENAI"],
            'huggingface_api_key' : os.environ["API_KEY_HUGGINGFACE"]
        }
    
    def execute_scenario(self):
        # for model in self.__scenario.models:
        #     self.__query_model(model)
        self.__query_model('HuggingChat')
        # self.__query_model('HuggingFaceGPT2')
        # self.__query_model('HuggingFaceGPT2Large')
        # self.__query_model('HuggingFaceGPT2XLarge')
        # self.__query_model('HuggingFaceBlenderBot')
        # self.__query_model('HuggingFacePersonaGPT')
        # self.__query_model('HuggingFaceDialoGPT')
        # self.__query_model('HuggingFaceSmallRickSanchez')
        # self.__query_model('HuggingFaceRobertaBaseSquad2')
        # self.__query_model('HuggingFaceDistilbertBaseUncased')
        # self.__query_model('OpenAITextCurie001')
        # self.__query_model('OpenAITextBabbage001')
        # self.__query_model('OpenAITextAda001')
        self.__query_model('OpenAITextDaVinci003')
        self.__query_model('OpenAIGPT35Turbo0301')
        self.__query_model('OpenAIGPT35Turbo0613')
        self.__query_model('OpenAIGPT35Turbo')
        # self.__query_model('OpenAIGPT35Turbo16k')
        self.__query_model('OpenAIGPT40314')
        self.__query_model('OpenAIGPT40613')
        self.__query_model('OpenAIGPT4')
    
    def __query_model(self, model: str):
        print(f'querying {model}...')
        llmservice: LLMService = llm_factory.factory.create(model, **self.__config)
        llmservice.temperature = self.__scenario.temperature
        llmservice.tokens = self.__scenario.tokens
        provider = llmservice.provider
        prompt: Prompt
        for prompt in self.__scenario.prompts:
            try:
                prompt.execute(llmservice)
                evaluation = prompt.evaluate()
                self.__update_responses(provider, model, prompt)
                self.__update_evaluations(provider, model, prompt, evaluation)
            except Exception as ex:
                self.__update_responses_error(provider, model, prompt, ex.args[0])
                self.__update_evaluations_error(provider, model, prompt, ex.args[0])
                time.sleep(10) # sleep for 10 seconds to allow the model to restore
        print('done')
    
    def __update_responses(self, provider, model, prompt: Prompt):
        if len(prompt.responses) == 0:
            self.responses.append(ResponseView(provider, model, 'Template: ' + prompt.template, 'No response provided'))
        else:
            for prompt_response in prompt.responses:
                self.responses.append(ResponseView(provider, model, prompt_response.instance, prompt_response.response))
                # print(f'{prompt_response.instance}: {prompt_response.response}')

    def __update_evaluations(self, provider, model, prompt: Prompt, evaluation: str):
        self.evaluations.append(EvaluationView(provider, model, prompt.concern, prompt.type, prompt.assessment, prompt.template, prompt.oracle_operation, prompt.oracle_prediction, evaluation))

    def __update_responses_error(self, provider, model, prompt: Prompt, error_msg):
        for prompt_response in prompt.responses:
            self.responses.append(ResponseView(provider, model, prompt_response.instance, 'ERROR: ' + error_msg))
            # print(f'{prompt_response.instance}: ERROR - {error_msg}')

    def __update_evaluations_error(self, provider, model, prompt: Prompt, error_msg):
        self.evaluations.append(EvaluationView(provider, model, prompt.concern, prompt.type, prompt.assessment, prompt.template, prompt.oracle_operation, prompt.oracle_prediction, 'ERROR: ' + error_msg))
