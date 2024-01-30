from enum import Enum
from itertools import product, count
import re
from langbite.llm_services.llm_service import LLMService
from langbite.prompt_response import PromptResponse
from langbite.oracles.oracle import Oracle
from langbite.oracles.sentiment_analyzer_oracle import SentimentAnalyzerOracle


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
        # TODO: markup should be an attribute of the ethical concern
        if concern == 'racism': markup = 'SKIN_COLOR'
        if concern == 'sexism': markup = 'GENDER'
        if concern == 'lgtbiqphobia': markup = 'SEXUAL_ORIENTATION'
        if concern == 'religion': markup = 'RELIGION'
        if concern == 'xenophobia': markup = 'COUNTRY'
        if concern == 'ageism': markup = 'AGE'

        if len(communities) > 0:
            # self.__instances = self.__replace_markups(markup, communities)
            if self.template.count('{' + markup) == 1:
                markup = '{' + markup + '}'
                raw_list = [self.template.replace(markup, community) for community in communities]
            else: # let's have 2 max, yet
                markup1 = '{' + markup + '1}'
                markup2 = '{' + markup + '2}'
                raw_list = []
                for community1 in communities:
                    for community2 in communities:
                        if community1 != community2:
                            raw_list.append(self.template.replace(markup1, community1).replace(markup2, community2))
            self.__instances = list(set(raw_list))
        else:
            self.__instances = [self.template]
    
    def set_oracle_delta(self, delta):
        self.__oracle.set_delta(delta)
    
    def set_oracle_reinforce_failed_evaluation(self, reinforce: bool):
        self.__oracle.reinforce_failed = reinforce
    
    def execute(self, llmservice: LLMService):
        # execute prompt instances and collect responses
        responses = []
        for instance in self.instances:
            prompt = self.__get_instantiated_prompt(instance)
            response = llmservice.execute_prompt(prompt)
            responses.append(PromptResponse(instance, response))
        self.__responses = responses

    def evaluate(self, llmsentiment: SentimentAnalyzerOracle) -> str:
        #if (self._responses is None or self._oracle is None): return "none"
        result = self.__oracle.evaluate(self.__responses, llmsentiment)
        return result
    
    def __get_instantiated_prompt(self, instance) -> str:
        if self.has_prefix:
            prompt = f'{self.task_prefix} {self.__prompt_delimiter}{instance}{self.__prompt_delimiter}. {self.__output_formatting}'
        else:
            prompt = f'{instance} {self.__output_formatting}'
        return prompt
    
    def __replace_markups(self, markup, communities):
        # define a regular expression pattern to match content within curly brackets
        # and find all markups in the template
        pattern = r'\{.*?\}'
        markups = re.findall(pattern, self.template)

        # generate all combinations
        combinations = product(communities, repeat=len(markups))
        instances = [
            re.sub(pattern, lambda x, replacements=combo, counter=count(): replacements[next(counter)], self.template)
            for combo in combinations
            # exclude combinations comparing the same community
            if len(set(combo)) == len(combo)
        ]

        return instances
