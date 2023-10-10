from enum import Enum
import re
from llm_service import LLMService
import time
from oracle import Oracle


# -----------------------------------------------------------------------
# markups
# -----------------------------------------------------------------------

KEY_SKIN_COLOR = "{SKIN_COLOR}"
KEY_OCCUPATION = "{JOB_TITLE}"
KEY_NAME = "{NAME}"
KEY_GENDER = "{GENDER}"
KEY_LOCATION = "{LOCATION}"

# -----------------------------------------------------------------------
# sensitive inputs
# -----------------------------------------------------------------------

#GENDERS = ["man", "woman"]
#SKIN_COLORS = ["white", "brown", "black", "yellow"]
# occupations = pandas.read_csv('resources/occupations.csv')['occupation'].to_list()
# names = pandas.read_csv('resources/names.csv')['name'].to_list()
# nationalities = ["Spanish", "Chinese", "American", "Italian", "British", "Russian", "Arabian", "South African", "Nigerian"]

# -----------------------------------------------------------------------
# enumerations
# -----------------------------------------------------------------------

ConcernKind = Enum('ConcernKind', 'gender race politics religion nationality')
PromptKind = Enum('PromptKind', 'open adversarial')
AssessmentKind = Enum('AssessmentKind', 'observational utopian')

class PromptResponse:

    @property
    def provider(self):
        return self._provider
    
    @property
    def model(self):
        return self._model
    
    @property
    def instance(self):
        return self._instance
    
    @property
    def response(self):
        return self._response
    
    @response.setter
    def response(self, value):
        self._response = re.sub('\n','',value).lower()
    
    @property
    def execution_time(self):
        return self._timestamp

    def __init__(self, provider, model, instance, response):
        self._provider = provider
        self._model = model
        self._instance = instance
        self.response = response
        self._timestamp = time.localtime()

class Prompt:
    
    prompt_delimiter = f'"""'

    @property
    def prompt_id(self):
        return self._id
    
    @property
    def responses(self) -> list[PromptResponse]:
        return self._responses
    
    @property
    def responses_text(self) -> list[str]:
        return list(response.response for response in self._responses)
    
    @property
    def task_prefix(self):
        return self._task_prefix
    
    @task_prefix.setter
    def task_prefix(self, value):
        if value is not None: self._task_prefix = f'{value} The sentence is delimited by {self.prompt_delimiter}.'
        else: self._task_prefix = None
    
    @property
    def has_prefix(self):
        return self._task_prefix is not None
    
    @property
    def template(self):
        return self._template
    
    @property
    def concern(self):
        return self._concern
    
    @property
    def type(self):
        return self._type
    
    @property
    def assessment(self):
        return self._assessment
    
    @property
    def execution_provider(self):
        return self._execution_provider
    
    @property
    def execution_model(self):
        return self._execution_model
    
    @property
    def oracle_operation(self):
        return self._oracle.operation
    
    @property
    def oracle_prediction(self):
        return self._oracle.expected_value
            
    def __init__(self, id, concern: ConcernKind, type: PromptKind, assessment: AssessmentKind, task_prefix, template, output_formatting, oracle: Oracle):
        self._id = id
        self._concern = concern
        self._type = type
        self._assessment = assessment
        self.task_prefix = task_prefix
        self._template = template
        self._output_formatting = output_formatting
        self._oracle = oracle
        #self._instances = self.instantiate()
        self._responses = [PromptResponse]
    
    def instantiate(self, concern, communities):
        # TODO: esta es una forma ultra cutre de instanciar la plantilla !!!!!
        if concern == 'race': concern = 'SKIN_COLOR'
        if concern == 'gender': concern = 'GENDER'
        # TODO: esta es una forma ultra cutre de hacer combinaciones de 2 communities !!!!!
        if self._template.count('{' + concern) == 1:
            markup = '{' + concern + '}'
            raw_list = [self._template.replace(markup, community) for community in communities]
        else: # asumimos 2, de momento
            markup1 = '{' + concern + '1}'
            markup2 = '{' + concern + '2}'
            raw_list = []
            for community1 in communities:
                for community2 in communities:
                    if community1 != community2:
                        raw_list.append(self._template.replace(markup1, community1).replace(markup2, community2))
        self._instances = list(set(raw_list))
    
    def execute(self, llmservice: LLMService):
        # trace last execution
        self._execution_provider = llmservice.provider
        self._execution_model = llmservice.model
        # execute prompt instances and collect responses
        responses = []
        for instance in self._instances:
            prompt = self.get_instantiated_prompt(instance)
            response = llmservice.execute_prompt(prompt)
            responses.append(PromptResponse(llmservice.provider, llmservice.model, instance, response))
        self._responses = responses

    def evaluate(self) -> str:
        #if (self._responses is None or self._oracle is None): return "none"
        result = self._oracle.evaluate(self.responses_text)
        return result
    
    def get_instantiated_prompt(self, instance) -> str:
        if self.has_prefix:
                prompt = f'{self.task_prefix} {self.prompt_delimiter}{instance}{self.prompt_delimiter}. {self._output_formatting}'
        else:
            prompt = f'{instance} {self._output_formatting}'
        return prompt