from prompt import Prompt
from random import sample

class TestScenario:

    @property
    def prompts(self) -> [Prompt]:
        return self._prompts
    
    @prompts.setter
    def prompts(self, value: [Prompt]):
        self.__select_prompts(value)
        self.__instantiate_prompts()

    def __init__(self, cfg):
        self._timestamp = cfg['timestamp']
        self._temperature = cfg['temperature']
        self._tokens = cfg['tokens']
        self._num_tests = cfg['numTests']
        self._ethical_requirements = cfg['requirements']
    
    def __select_prompts(self, prompts: [Prompt]):
        result = []
        for req in self._ethical_requirements:
            concern = req['concern']
            # filter prompts by concern and prompt type
            # and then select according to num tests specified
            prompt_types = [prompt_type.lower() for prompt_type in req['prompts']]
            by_prompt_type = []
            for prompt_type in prompt_types:
                by_prompt_type = by_prompt_type + [prompt for prompt in prompts if prompt.concern == concern and prompt.type == prompt_type]
            # filter prompts by concern and assessment type
            # and then select according to num tests specified
            assessment_types = [assessment_type.lower() for assessment_type in req['assessments']]
            by_assessment_type = []
            for assessment_type in assessment_types:
                by_assessment_type = by_assessment_type + [prompt for prompt in prompts if prompt.concern == concern and prompt.assessment == assessment_type]
            # add all filtered prompts from the concern to the final list
            result = result + self.__sample_list(by_prompt_type) + self.__sample_list(by_assessment_type)
        self._prompts = result
    
    def __sample_list(self, prompt_list: list[Prompt]):
        if len(prompt_list) > self._num_tests: prompt_list = sample(prompt_list, self._num_tests)
        return prompt_list
    
    def __instantiate_prompts(self):
        for req in self._ethical_requirements:
            concern = req['concern']
            communities = req['communities']
            prompt: Prompt
            for prompt in self._prompts:
                if (prompt.concern == concern):
                    prompt.instantiate(concern, communities)