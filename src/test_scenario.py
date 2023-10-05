from prompt import Prompt

class TestScenario:

    @property
    def prompts(self) -> [Prompt]:
        return self._prompts
    
    @prompts.setter
    def prompts(self, value: [Prompt]):
        self.set_prompts(value)
        self.instantiate_prompts()

    def __init__(self, cfg):
        self._timestamp = cfg['timestamp']
        self._temperature = cfg['temperature']
        self._tokens = cfg['tokens']
        self._ethical_requirements = cfg['requirements']
    
    def set_prompts(self, prompts: [Prompt]):
        result = []
        for req in self._ethical_requirements:
            concern = req['concern']
            prompt_types = [prompt_type.lower() for prompt_type in req['prompts']]
            assessment_types = [assessment_type.lower() for assessment_type in req['assessments']]
            filtered = [prompt for prompt in prompts if prompt.concern == concern and prompt.type in prompt_types and prompt.assessment in assessment_types]
            result = result + filtered
        self._prompts = result
    
    def instantiate_prompts(self):
        for req in self._ethical_requirements:
            concern = req['concern']
            communities = req['communities']
            for prompt in self._prompts:
                if (prompt.concern == concern):
                    prompt.instantiate(concern, communities)