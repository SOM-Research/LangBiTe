from langbite.llm_services import llm_factory
from langbite.llm_services.llm_openai_factory import OpenAIChatService
import langbite.io_managers.prompt_io_manager as PromptIOManager
import json


class Augmentator:

    START = 6

    @property
    def additional_instructions(self):
        return self.__additional_instructions
    
    @additional_instructions.setter
    def additional_instructions(self, value):
        if value is not None:
            self.__additional_instructions = '\n\n'.join(f"{i+self.START}. {s}" for i, s in enumerate(value))
        else:
            self.__additional_instructions = ''
    
    def __init__(self, model, num_templates, language, additional_instructions, **config):
        self.__llm_service: OpenAIChatService = llm_factory.factory.create(model, **config)
        self.__num_templates = num_templates
        self.__language = language
        self.additional_instructions = additional_instructions

    def execute(self, concern, communities, context, scenarios, fake_markup):
        augmentation_prompt_template = PromptIOManager.load_augmentation_prompt()
        augmentation_prompt = augmentation_prompt_template.format(
            concern=concern,
            sensitive_communities=', '.join(communities),
            num_templates=self.__num_templates,
            #language=language,
            fake_markup=fake_markup,
            first_community=communities[0],
            second_community=communities[1],
            context=context,
            scenarios=scenarios,
            additional_instructions=self.additional_instructions)
        result = []
        num_tries = 0
        executed = False
        while (num_tries < 3 and not executed):
            try:
                response = self.__llm_service.execute_prompt(augmentation_prompt)
                response = self.__remove_reasoning(response)
                result = json.loads(response)
                executed = True
            except Exception as ex:
                num_tries += 1
        return result

    def __remove_reasoning(self, response: str) -> str:
        inner_str = '[' + response.split('[')[len(response.split('[')) -1 ].split(']')[0] +']'
        return inner_str
