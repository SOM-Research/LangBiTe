from langbite.prompt import Prompt
from langbite.ethical_requirement import EthicalRequirements, EthicalRequirement
from random import sample
import langbite.utils

class TestScenario:

    @property
    def timestamp(self):
        return self.__timestamp
    
    @timestamp.setter
    def timestamp(self, value):
        self.__timestamp = value
    
    @property
    def temperature(self):
        return self.__temperature
    
    @temperature.setter
    def temperature(self, value):
        self.__temperature = value
    
    @property
    def tokens(self):
        return self.__tokens
    
    @tokens.setter
    def tokens(self, value):
        self.__tokens = value
    
    @property
    def num_tests(self):
        return self.__num_tests
    
    @num_tests.setter
    def num_tests(self, value):
        self.__num_tests = value

    @property
    def num_retries(self):
        return self.__num_retries
    
    @num_retries.setter
    def num_retries(self, value):
        self.__num_retries = value

    @property
    def use_llm_eval(self):
        return self.__use_llm_eval
    
    @use_llm_eval.setter
    def use_llm_eval(self, value):
        self.__use_llm_eval = value
    
    @property
    def ethical_requirements(self):
        return self.__ethical_requirements
    
    @ethical_requirements.setter
    def ethical_requirements(self, value):
        self.__ethical_requirements = value

    @property
    def models(self):
        return self.__models
    
    @models.setter
    def models(self, value):
        self.__models = value

    @property
    def prompts(self) -> list[Prompt]:
        return self.__prompts
    
    @property
    def languages(self):
        return self.__languages
    
    @languages.setter
    def languages(self, value):
        self.__languages = value
    
    @prompts.setter
    def prompts(self, value: list[Prompt]):
        self.__select_prompts(value)
        self.__instantiate_prompts()

    def __init__(self, cfg):
        self.timestamp = cfg['timestamp']
        self.temperature = cfg['temperature']
        self.tokens = cfg['tokens']
        self.num_tests = cfg['nTemplates']
        self.num_retries = cfg['nRetries']
        self.use_llm_eval = cfg['useLLMEval']
        self.ethical_requirements = EthicalRequirements(cfg['requirements']).requirements
        self.languages = self.__set_languages()
        self.models = cfg['aiModels']
    
    def __set_languages(self):
        return langbite.utils.merge_unique([e.languages for e in self.ethical_requirements])
    
    def __select_prompts(self, prompts: list[Prompt]):
        result = []
        req: EthicalRequirement
        for req in self.ethical_requirements:
            for language in req.languages:
                concern = req.concern
                input_types = [input_type for input_type in req.inputs]
                reflection_types = [reflection_type for reflection_type in req.reflections]
                for input_type in input_types:
                    for reflection_type in reflection_types:
                        # filter prompts by concern, prompt type and assessment type
                        temp = [prompt for prompt in prompts if
                            prompt.concern == concern and prompt.input_type == input_type and prompt.reflection_type == reflection_type and
                            prompt.language == language]
                        # and then select according to num tests specified
                        result = result + self.__sample_list(temp)
                # 1. assign delta as per requirement
                # 2. set whether the req forces sentiment analysis to re-check failed tests
                prompt: Prompt
                for prompt in result:
                    prompt.set_oracle_delta(req.delta)
                    prompt.set_oracle_reinforce_failed_evaluation(self.use_llm_eval)
        self.__prompts = result
    
    def __sample_list(self, prompt_list: list[Prompt]):
        if len(prompt_list) > self.num_tests: prompt_list = sample(prompt_list, self.num_tests)
        return prompt_list
    
    def __instantiate_prompts(self):
        req: EthicalRequirement
        for req in self.ethical_requirements:
            # concern = req.concern
            # markup = req.markup
            # communities = []
            # if 'communities' in req: communities = req.communities
            prompt: Prompt
            for prompt in self.__prompts:
                if (prompt.concern == req.concern):
                    prompt.instantiate(req.markup, req.communities)