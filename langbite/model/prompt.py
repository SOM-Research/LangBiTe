from enum import Enum
from itertools import permutations
import re
from langbite.llm_services.llm_service import LLMService
from langbite.model.prompt_response import PromptResponse
from langbite.oracles.oracle import Oracle
from langbite.oracles.sentiment_analyzer_oracle import SentimentAnalyzerOracle


# -----------------------------------------------------------------------
# constants
# -----------------------------------------------------------------------

PROMPT_DELIMITER = f'"""'

MARKUP_START = '{'
MARKUP_END = '}'

# MARKUPS = {
#     'racism': 'SKIN_COLOR',
#     'sexism': 'GENDER',
#     'lgtbiqphobia': 'SEXUAL_ORIENTATION',
#     'religion': 'RELIGION',
#     'xenophobia': 'COUNTRY',
#     'ageism': 'AGE',
#     'politics': 'POLITICAL_VIEW',
#     'sexism_ambiguity': 'PRONOUN'
# }

# -----------------------------------------------------------------------
# enumerations
# -----------------------------------------------------------------------

ConcernKind = Enum('ConcernKind', 'ageism lgtbiqphobia politics racism religion sexism xenophobia sexism_ambiguity')
InputKind = Enum('InputKind', 'constrained verbose')
ReflectionKind = Enum('ReflectionKind', 'observational utopian')

# -----------------------------------------------------------------------
# main class
# -----------------------------------------------------------------------

class Prompt:

    @property
    def prompt_id(self):
        return self.__id
    
    @property
    def language(self):
        return self.__language
    
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
        if value is not None: self.__task_prefix = f'{value} The sentence is delimited by {PROMPT_DELIMITER}.'
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
    def input_type(self):
        return self.__input_type
    
    @property
    def reflection_type(self):
        return self.__reflection_type
    
    @property
    def oracle_operation(self):
        return self.__oracle.operation
    
    @property
    def oracle_prediction(self):
        return self.__oracle.expected_value
            
    def __init__(self, id, concern, input_type: InputKind, reflection_type: ReflectionKind, language, task_prefix, template, output_formatting, oracle: Oracle):
        self.__id = id
        self.__concern = concern
        self.__input_type = input_type
        self.__reflection_type = reflection_type
        self.__language = language
        self.task_prefix = task_prefix
        self.__template = template
        self.__output_formatting = output_formatting
        self.__oracle = oracle
        self.__responses = [PromptResponse]
    
    def instantiate(self, markup, communities):
        # markup might be an attribute of the ethical concern
        # markup = MARKUPS[concern]

        if len(communities) > 0:
            lang_communities = communities[self.language]
            if len(lang_communities) > 0:
                self.__instances = self.__replace_markups(markup, lang_communities)
            else:
                self.__instances = [self.template]
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
        result = self.__oracle.evaluate(self.__responses, llmsentiment)
        return result
    
    def __get_instantiated_prompt(self, instance) -> str:
        if self.has_prefix:
            prompt = f'{self.task_prefix} {PROMPT_DELIMITER}{instance}{PROMPT_DELIMITER}. {self.__output_formatting}'
        else:
            prompt = f'{instance} {self.__output_formatting}'
        return prompt
    
    def __replace_markups(self, markup_root, communities):
        # define a regular expression pattern to match content within curly brackets
        # and find all distinct markups in the template
        pattern = re.compile(f'{MARKUP_START}{markup_root}[0-9]*?{MARKUP_END}')
        markups = set(pattern.findall(self.template))

        # generate all combinations of communities according to number of markups
        # excluding combinations comparing a community to itself
        communities_combos = [combo for combo in permutations(communities, len(markups)) if len(set(combo)) == len(combo)]

        instances = []
        for combo in communities_combos:
            instance = self.template
            for markup, community in zip(markups, combo):
                instance = instance.replace(markup, community)
            instances.append(instance)

        return instances
