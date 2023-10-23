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
# enumerations
# -----------------------------------------------------------------------

ConcernKind = Enum('ConcernKind', 'gender race politics religion nationality')
PromptKind = Enum('PromptKind', 'open adversarial')
AssessmentKind = Enum('AssessmentKind', 'observational utopian')

class PromptResponse:
    
    @property
    def instance(self) -> str:
        return self.__instance
    
    @property
    def response(self) -> str:
        return self.__response
    
    @response.setter
    def response(self, value: str):
        self.__response = re.sub('\n','',value.strip()).lower()
    
    @property
    def execution_time(self):
        return self.__timestamp

    def __init__(self, instance, response):
        self.__instance = instance
        self.response = response
        self.__timestamp = time.localtime()

class Prompt:
    
    __prompt_delimiter = f'"""'

    @property
    def prompt_id(self):
        return self.__id
    
    @property
    def instances(self) -> list[str]:
        return self.__instances
    
    @property
    def responses(self) -> list[PromptResponse]:
        return self.__responses
    
    @property
    def responses_text(self) -> list[str]:
        return list(response.response for response in self.responses)
    
    @property
    def task_prefix(self):
        return self.__task_prefix
    
    @task_prefix.setter
    def task_prefix(self, value):
        if value is not None: self.__task_prefix = f'{value} The sentence is delimited by {self.__prompt_delimiter}.'
        else: self.__task_prefix = None
    
    @property
    def has_prefix(self):
        return self.__task_prefix is not None
    
    @property
    def template(self) -> str:
        return self.__template
    
    @property
    def concern(self):
        return self.__concern
    
    @property
    def type(self):
        return self.__type
    
    @property
    def assessment(self):
        return self.__assessment
    
    @property
    def oracle_operation(self):
        return self.__oracle.operation
    
    @property
    def oracle_prediction(self):
        return self.__oracle.expected_value
            
    def __init__(self, id, concern: ConcernKind, type: PromptKind, assessment: AssessmentKind, task_prefix, template, output_formatting, oracle: Oracle):
        self.__id = id
        self.__concern = concern
        self.__type = type
        self.__assessment = assessment
        self.task_prefix = task_prefix
        self.__template = template
        self.__output_formatting = output_formatting
        self.__oracle = oracle
        self.__responses = [PromptResponse]
    
    def instantiate(self, concern, communities):
        # TODO: esta es una forma ultra cutre de instanciar la plantilla !!!!!
        if concern == 'racism': markup = 'SKIN_COLOR'
        if concern == 'sexism': markup = 'GENDER'
        if concern == 'lgtbiqphobia': markup = 'SEXUAL_ORIENTATION'
        if concern == 'religion': markup = 'RELIGION'
        # TODO: esta es una forma ultra cutre de hacer combinaciones de 2 communities !!!!!
        if len(communities) > 0:
            if self.template.count('{' + concern) == 1:
                markup = '{' + markup + '}'
                raw_list = [self.template.replace(markup, community) for community in communities]
            else: # asumimos 2, de momento
                markup1 = '{' + markup + '1}'
                markup2 = '{' + markup + '2}'
                raw_list = []
                for community1 in communities:
                    for community2 in communities:
                        if community1 != community2:
                            raw_list.append(self.template.replace(markup1, community1).replace(markup2, community2))
            self.__instances = list(set(raw_list))
        else:
            self.__instances = self.template
    
    def set_oracle_delta(self, delta):
        self.__oracle.set_delta(delta)
    
    def execute(self, llmservice: LLMService):
        # execute prompt instances and collect responses
        responses = []
        for instance in self.instances:
            prompt = self.__get_instantiated_prompt(instance)
            response = llmservice.execute_prompt(prompt)
            responses.append(PromptResponse(instance, response))
        self.__responses = responses

    def evaluate(self) -> str:
        #if (self._responses is None or self._oracle is None): return "none"
        result = self.__oracle.evaluate(self.responses_text)
        return result
    
    def __get_instantiated_prompt(self, instance) -> str:
        if self.has_prefix:
                prompt = f'{self.task_prefix} {self.__prompt_delimiter}{instance}{self.__prompt_delimiter}. {self.__output_formatting}'
        else:
            prompt = f'{instance} {self.__output_formatting}'
        return prompt