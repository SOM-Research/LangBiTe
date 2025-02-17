from langbite.llm_services import llm_factory
from langbite.llm_services.llm_openai_factory import OpenAIChatService
import json
import langbite.io_managers.prompt_io_manager as PromptIOManager


class Augmentator:

    #AUGMENTATOR_MODEL = 'OpenAIGPT4oMini'

    __llm_service: OpenAIChatService = None
    
    def __init__(self, model, **config):
        self.__llm_service: OpenAIChatService = llm_factory.factory.create(model, **config)

    def execute(self, concern, communities, context, scenarios, num_templates, language, fake_markup):
        augmentation_prompt_template = PromptIOManager.load_augmentation_prompt()
        augmentation_prompt = augmentation_prompt_template.format(
            concern=concern,
            sensitive_communities=', '.join(communities),
            num_templates=num_templates,
            #language=language,
            fake_markup=fake_markup,
            first_community=communities[0],
            second_community=communities[1],
            context=context,
            scenarios=scenarios)
        result = json.loads(self.__llm_service.execute_prompt(augmentation_prompt))
        return result
