from test_scenario import TestScenario
from prompt import Prompt
import llm_factory
from dotenv import load_dotenv
import os
from view_model import EvaluationView, ResponseView

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
        for model in self.__scenario.models:
            self.__query_model(model)
        # self.__query_model('HuggingChat')
        # self.__query_model('HuggingFaceGPT2')
        # self.__query_model('HuggingFaceGPT2Large')
        # self.__query_model('HuggingFaceGPT2XLarge')
        # self.__query_model('OpenAITextDaVinci002')
        # self.__query_model('OpenAITextDaVinci003')
        # self.__query_model('OpenAIGPT35Turbo')
    
    def __query_model(self, model: str):
        print(f'querying {model}...')
        llmservice = llm_factory.factory.create(model, **self.__config)#, self.__scenario.temperature, self.__scenario.tokens)
        prompt: Prompt
        for prompt in self.__scenario.prompts:
            try:
                prompt.execute(llmservice)
                evaluation = prompt.evaluate()
                self.__update_responses(prompt)
                self.__update_evaluations(prompt, evaluation)
            except:
                self.__update_responses_error(prompt)
                self.__update_evaluations_error(prompt)
        print('done')
    
    def __update_responses(self, prompt: Prompt):
        if len(prompt.responses) == 0:
            self.responses.append(ResponseView(prompt.execution_provider, prompt.execution_model, 'Template: ' + prompt.template, 'No response provided'))
        else:
            for prompt_response in prompt.responses:
                self.responses.append(ResponseView(prompt_response.provider, prompt_response.model, prompt_response.instance, prompt_response.response))

    def __update_evaluations(self, prompt: Prompt, evaluation: str):
        self.evaluations.append(EvaluationView(prompt.execution_provider, prompt.execution_model, prompt.concern, prompt.type, prompt.assessment, prompt.template, prompt.oracle_operation, prompt.oracle_prediction, evaluation))

    def __update_responses_error(self, prompt: Prompt):
        for prompt_response in prompt.responses:
            self.responses.append(ResponseView(prompt_response.provider, prompt_response.model, prompt_response.instance, 'ERROR'))

    def __update_evaluations_error(self, prompt: Prompt):
        self.evaluations.append(EvaluationView(prompt.execution_provider, prompt.execution_model, prompt.concern, prompt.type, prompt.assessment, prompt.template, prompt.oracle_operation, prompt.oracle_prediction, 'ERROR'))
