from datetime import datetime
from langbite.io_managers import json_io_manager as JSONIOManager
from langbite.io_managers.reporting_io_manager import ReportingIOManager
import langbite.io_managers.secrets as Secrets
from langbite.template_augmentation.model import Augmentation, AugmentationPair, EthicalConcern, Context
from langbite.template_augmentation.llm_augmentator import Augmentator
import pandas as pd


class AugmentatorWrongStateException(Exception):
    '''Sorry, you haven't followed the expected workflow. The proper invoking sequence is: init LangBite, generate, execute and report.'''

class TemplateAugmentatorWorkflow:

    INIT = 0
    FETCHED = 1
    EXECUTED = 2

    def __init__(self):
        self.__status = TemplateAugmentatorWorkflow.INIT
    
    def check(self, expected_status):
        if self.__status != expected_status: raise AugmentatorWrongStateException
    
    def next(self):
        self.__status += 1


class TemplateAugmentator:

    FAKE_MARKUP = 'CHUMPINFLAS'

    @property
    def result(self):
        return self.__result

    def __init__(self, augmentation_pars=None, augmentation_file=None, contexts_from_resource_file=True):
        self.__result = []
        self.__augmentation_json = augmentation_pars
        self.__augmentation_file = augmentation_file
        self.__contexts_from_resource_file = contexts_from_resource_file
        self.__status = TemplateAugmentatorWorkflow()

    # ---------------------------------------------------------------------------------
    # Methods for fetching, executing and reporting augmentations
    # ---------------------------------------------------------------------------------

    def execute_full_scenario(self):
        self.fetch_augmentation()
        self.execute()
        self.report()


    def fetch_augmentation(self):
        self.__status.check(TemplateAugmentatorWorkflow.INIT)
        if self.__augmentation_file:
            self.__load_augmentations(JSONIOManager.load_augmentations(self.__augmentation_file))
        else:
            self.__load_augmentations(self.__augmentation_json)
        self.__status.next()


    def execute(self):
        self.__status.check(TemplateAugmentatorWorkflow.FETCHED)
        time_ini = datetime.now()

        api_keys = Secrets.load_api_keys()
        self.__augmentator = Augmentator(self.__augmentation.llm, self.__augmentation.num_templates, self.__augmentation.language, **api_keys)

        for aug in self.__augmentation.augmentations:
            self.__result += (self.__generate_templates(aug))

        time_end = datetime.now()
        print(f'Time elapsed for generating {len(self.__result)} prompt templates): ' + str(time_end - time_ini))
        self.__status.next()
    

    def report(self):
        self.__status.check(TemplateAugmentatorWorkflow.EXECUTED)
        df = pd.DataFrame.from_records(self.__result)
        #df.insert(0, 'context', df.pop('context'))
        df = df[['concern', 'input_type', 'reflection_type', 'task_prefix', 'prompt', 'output_formatting', 'oracle', 'oracle_prediction', 'context', 'scenario']]
        #df = df[['concern', 'context', 'scenario', 'prompt', 'output_formatting', 'oracle_prediction']]
        print(df)
        report = ReportingIOManager()
        report.write_output_file(df, 'augmentation')

    # ---------------------------------------------------------------------------------
    # Private methods
    # ---------------------------------------------------------------------------------

    def __load_augmentations(self, augmentation_json: str):
        self.__augmentation = Augmentation(**augmentation_json)
        concerns = [EthicalConcern(**item) for item in augmentation_json['concerns']]
        if self.__contexts_from_resource_file:
            contexts = [Context(**item) for item in JSONIOManager.load_contexts()]
        else:
            contexts = [Context(**item) for item in augmentation_json['contexts']]
        augmentations = [AugmentationPair(**item) for item in augmentation_json['augmentations']]
        for aug in augmentations:
            concern = next(item for item in concerns if item.concern == aug.concern)
            aug.markup = concern.markup
            aug.communities = concern.communities
            context = next(item for item in contexts if item.context == aug.context)
            aug.scenarios = context.scenarios
        self.__augmentation.augmentations = augmentations


    def __generate_templates(self, augmentation: AugmentationPair):

        print(f'Generating prompts for: {augmentation.context} ({augmentation.concern})')

        templates = self.__augmentator.execute(
            concern=augmentation.concern,
            communities=augmentation.communities,
            context=augmentation.context,
            scenarios=augmentation.scenarios,
            fake_markup=self.FAKE_MARKUP)

        for template in templates:
            # we use fake markups in the prompt not to alter (semantically, syntactically)
            # the generation of the templates
            if self.FAKE_MARKUP in template['prompt']:
                template['prompt'] = template['prompt'].replace(self.FAKE_MARKUP, augmentation.markup)
                oracle_prediction_prefix = '{"operation":"allEqualExpected","expected_value":["'
            else:
                oracle_prediction_prefix = '{"operation":"equal","expected_value":["'
            template['oracle_prediction'] = oracle_prediction_prefix + template['oracle_prediction'] + '"]}'

        new_keys = {
            'context': augmentation.context,
            'concern': augmentation.concern,
            'input_type': '',
            'reflection_type': '',
            'task_prefix': '',
            'oracle': 'expected value',
            'output_formatting': 'Do not use a JSON format for your response. Begin your answer with "Yes" or "No".' }
        
        result = [dict(item, **new_keys) for item in templates]
        return result
