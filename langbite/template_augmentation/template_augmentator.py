from langbite.io_managers import json_io_manager as JSONIOManager
import langbite.io_managers.secrets as Secrets
from langbite.template_augmentation.augmentation import Augmentation, EthicalConcern, Context
from langbite.template_augmentation.llm_augmentator import Augmentator

class TemplateAugmentator:

    FAKE_MARKUP = 'CHUMPINFLAS'

    def __init__(self, augmentations_file): #, contexts_file):
        self.__augmentations_file = augmentations_file
        #self.__contexts_file = contexts_file
        self.__api_keys = Secrets.load_api_keys()
        self.__augmentator = Augmentator(**self.__api_keys)
    
    def execute(self):
        result = []
        augmentations = JSONIOManager.load_augmentations(self.__augmentations_file)
        concerns = [EthicalConcern(**item) for item in augmentations['concerns']]
        #contexts = [Context(**item) for item in self.__augmentations['contexts']]
        contexts = [Context(**item) for item in JSONIOManager.load_contexts()]#self.__contexts_file)]
        for aug in augmentations['augmentations']:
            augmentation = Augmentation(**aug)
            concern = next(item for item in concerns if item.concern == augmentation.concern)
            augmentation.markup = concern.markup
            augmentation.communities = concern.communities
            context = next(item for item in contexts if item.context == augmentation.context)
            augmentation.scenarios = context.scenarios
            result += (self.__generate_templates(augmentation))
        return result
    
    def __generate_templates(self, augmentation: Augmentation):

        print(f'Generating prompts for: {augmentation.context}')

        templates = self.__augmentator.execute(
            concern=augmentation.concern,
            communities=augmentation.communities,
            context=augmentation.context,
            scenarios=augmentation.scenarios,
            num_templates=augmentation.num_templates,
            fake_markup=self.FAKE_MARKUP)

        for template in templates:
            # we use fake markups in the prompt not to alter (semantically, syntactically)
            # the generation of the templates
            template['prompt'] = template['prompt'].replace(self.FAKE_MARKUP, augmentation.markup)
            template['oracle_prediction'] = '{"operation":"allEqualExpected","expected_value":["' + template['oracle_prediction'] + '"]}'

        new_keys = {
            'context': augmentation.context,
            'concern': augmentation.concern,
            'input_type': '',
            'reflection_type': '',
            'task_prefix': '',
            'oracle': 'expected value',
            'output_formatting': '' }
        result = [dict(item, **new_keys) for item in templates]
        return result
