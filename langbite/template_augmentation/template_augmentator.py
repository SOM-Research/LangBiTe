from langbite.io_managers import json_io_manager as JSONIOManager
import langbite.io_managers.secrets as Secrets
from langbite.template_augmentation.augmentation import Augmentation, EthicalConcern, Context
from langbite.template_augmentation.llm_augmentator import Augmentator
import pandas as pd
from langbite.io_managers.reporting_io_manager import ReportingIOManager

class AugmentatorWrongStateException(Exception):
    '''Sorry, you haven't followed the expected workflow. The proper invoking sequence is: init LangBite, generate, execute and report.'''

class TemplateAugmentator:

    FAKE_MARKUP = 'CHUMPINFLAS'

    def __init__(self, augmentation_pars=None, augmentations_file=None, contexts_from_resource_file=True):
        self.__augmentations = augmentation_pars
        self.__augmentations_file = augmentations_file
        self.__contexts_from_resource_file = contexts_from_resource_file
        self.__current_status = 0

    # ---------------------------------------------------------------------------------
    # Methods for fetching, executing and reporting augmentations
    # ---------------------------------------------------------------------------------

    def execute_full_scenario(self):
        self.fetch_augmentation()
        self.execute()
        self.report()

    def fetch_augmentation(self):
        if (self.__current_status != 0): raise AugmentatorWrongStateException
        if self.__augmentations_file:
            self.__augmentations = JSONIOManager.load_augmentations(self.__augmentations_file)
        if self.__contexts_from_resource_file:
            self.__contexts = [Context(**item) for item in JSONIOManager.load_contexts()]#self.__contexts_file)]
        else:
            self.__contexts = [Context(**item) for item in self.__augmentations['contexts']]
        self.__current_status = 1
    
    def execute(self):
        if (self.__current_status != 1): raise AugmentatorWrongStateException
        self.__result = []
        concerns = [EthicalConcern(**item) for item in self.__augmentations['concerns']]
        for aug in self.__augmentations['augmentations']:
            augmentation = Augmentation(**aug)
            concern = next(item for item in concerns if item.concern == augmentation.concern)
            augmentation.markup = concern.markup
            augmentation.communities = concern.communities
            context = next(item for item in self.__contexts if item.context == augmentation.context)
            augmentation.scenarios = context.scenarios
            self.__result += (self.__generate_templates(augmentation))
        self.__current_status = 2
    
    def report(self):
        if (self.__current_status != 2): raise AugmentatorWrongStateException
        df = pd.DataFrame.from_records(self.__result)
        #df.insert(0, 'context', df.pop('context'))
        df = df[['concern', 'input_type', 'reflection_type', 'task_prefix', 'prompt', 'output_formatting', 'oracle', 'oracle_prediction', 'context', 'scenario']]
        print(df)
        report = ReportingIOManager()
        report.write_output_file(df, 'augmentation')

    # ---------------------------------------------------------------------------------
    # Private methods
    # ---------------------------------------------------------------------------------

    def __generate_templates(self, augmentation: Augmentation):

        api_keys = Secrets.load_api_keys()
        augmentator = Augmentator(**api_keys)

        print(f'Generating prompts for: {augmentation.context}')

        templates = augmentator.execute(
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
