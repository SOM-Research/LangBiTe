from langbite.prompt import Prompt
from random import sample

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
    def prompts(self) -> [Prompt]:
        return self.__prompts
    
    @prompts.setter
    def prompts(self, value: [Prompt]):
        self.__select_prompts(value)
        self.__instantiate_prompts()

    def __init__(self, cfg):
        self.timestamp = cfg['timestamp']
        self.temperature = cfg['temperature']
        self.tokens = cfg['tokens']
        self.num_tests = cfg['numTests']
        self.ethical_requirements = cfg['requirements']
        self.models = cfg['aiModels']
    
    def __select_prompts(self, prompts: [Prompt]):
        result = []
        for req in self.ethical_requirements:
            concern = req['concern']
            prompt_types = [prompt_type.lower() for prompt_type in req['prompts']]
            assessment_types = [assessment_type.lower() for assessment_type in req['assessments']]
            for prompt_type in prompt_types:
                for assessment_type in assessment_types:
                    # filter prompts by concern, prompt type and assessment type
                    temp = [prompt for prompt in prompts if prompt.concern == concern and prompt.type == prompt_type and prompt.assessment == assessment_type]
                    # and then select according to num tests specified
                    result = result + self.__sample_list(temp)
            # 1. assign delta as per requirement
            # 2. set whether the req forces sentiment analysis to re-check failed tests
            prompt: Prompt
            for prompt in result:
                prompt.set_oracle_delta(req['delta'])
                prompt.set_oracle_reinforce_failed_evaluation(req['reinforceFailed'])
        self.__prompts = result
    
    def __sample_list(self, prompt_list: list[Prompt]):
        if len(prompt_list) > self.num_tests: prompt_list = sample(prompt_list, self.num_tests)
        return prompt_list
    
    def __instantiate_prompts(self):
        for req in self.ethical_requirements:
            concern = req['concern']
            communities = []
            if 'communities' in req: communities = req['communities']
            prompt: Prompt
            for prompt in self.__prompts:
                if (prompt.concern == concern):
                    prompt.instantiate(concern, communities)