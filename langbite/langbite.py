# --- -------------------------------------------------------------------
# --- LangBiTe: BIAS TESTER FOR LARGE LANGUAGE MODELS
# ---
# --- A tool for testing biases in large language models.
# --- Includes a library of prompts to test bias in
# --- gender, race / skin color, nationality, politics and religion.
# --- Prompts a large language model and assess the output
# --- trying to detect sensitive words and/or unexpected
# --- unethical responses.
# --- -------------------------------------------------------------------
from importlib.resources import files

from langbite.io_managers.scenario_io_manager import ScenarioIOManager
from langbite.io_managers.prompt_io_manager import CSVPromptIOManager, JSONPromptIOManager
from langbite.io_managers.reporting_io_manager import ReportingIOManager
from langbite.global_evaluation import GlobalEvaluator
from langbite.test_scenario import TestScenario
from langbite.test_execution import TestExecution
from langbite.prompt import Prompt
from datetime import datetime
from abc import abstractmethod


class RequirementsFileRequiredException(Exception):
    '''Sorry, you must provide a requirements file name.'''

class WrongStateException(Exception):
    '''Sorry, you haven't followed the expected workflow. The proper invoking sequence is: init LangBite, generate, execute and report.'''

class AbstractLangBiTe:

    # ---------------------------------------------------------------------------------
    # Public and private properties
    # ---------------------------------------------------------------------------------

    @property
    def requirements_file(self):
        return self.__requirements_file
    
    @requirements_file.setter
    def requirements_file(self, value):
        self.__requirements_file = value

    @property
    def requirements_dict(self):
        return self.__requirements_dict

    @requirements_dict.setter
    def requirements_dict(self, value):
        self.__requirements_dict = value

    @property
    def __requirements_file_empty(self):
        return (not self.__requirements_file or not self.__requirements_file.strip()) and not self.requirements_dict
    
    # very simple state machine
    # 0 = initiated
    # 1 = scenarios loaded and prompts selected
    # 2 = tests executed and evaluations collected

    @property
    def __current_status(self):
        return self.__current_internal_status
    
    @__current_status.setter
    def __current_status(self, value):
        self.__current_internal_status = value

    @property
    def evaluations(self):
        return self.__evaluations

    @property
    def responses(self):
        return self.__responses

    # ---------------------------------------------------------------------------------
    # Internal and auxiliary methods
    # ---------------------------------------------------------------------------------

    def __init__(self, file=None, file_dict=None):
        self.__requirements_file = file
        self.__requirements_dict = file_dict
        self.__current_status = 0

    def __update_figures(self):
        self.__num_prompts = len(self.__test_scenario.prompts)
        self.__num_instances = 0
        prompt: Prompt
        for prompt in self.__test_scenario.prompts:
            self.__num_instances = self.__num_instances + len(prompt.instances)
    
    # ---------------------------------------------------------------------------------
    # Methods for generating, executing and reporting test scenarios
    # ---------------------------------------------------------------------------------

    def execute_full_scenario(self):
        self.generate()
        self.execute()
        self.report()

    @abstractmethod
    def load_prompts(self, prompt_io):
        pass
    
    
    def generate(self):
        if (self.__current_status != 0): raise WrongStateException
        if (self.__requirements_file_empty): raise RequirementsFileRequiredException
        # load test scenario
        scenario_io = ScenarioIOManager()
        if self.requirements_file:
            self.__test_scenario = TestScenario(scenario_io.load_scenario(self.requirements_file))
        elif self.requirements_dict:
            self.__test_scenario = TestScenario(self.requirements_dict)
    
        # test generation
        self.__test_scenario.prompts = self.load_prompts()
        # aux: for output reasons
        self.__update_figures()
        self.__current_status = 1
    
    def execute(self):
        if (self.__current_status != 1): raise WrongStateException
        time_ini = datetime.now()
        # test execution and evaluation
        print("TEST SCENARIO ", self.__test_scenario)
        transaction = TestExecution(self.__test_scenario)
        transaction.execute_scenario()
        self.__responses = transaction.responses
        self.__evaluations = transaction.evaluations
        time_end = datetime.now()
        print(f'Time elapsed for executing {self.__num_instances} instances (from {self.__num_prompts} prompt templates): ' + str(time_end - time_ini))
        self.__current_status = 2

    def report(self, path=None):
        if (self.__current_status != 2): raise WrongStateException
        global_evaluator = GlobalEvaluator()
        global_evaluation = global_evaluator.evaluate(self.__evaluations, self.__test_scenario.ethical_requirements)
        reporting_io = ReportingIOManager()
        if path is not None:
            reporting_io.set_path(path)
        responses = reporting_io.write_responses(self.__responses)
        evaluations = reporting_io.write_evaluations(self.__evaluations)
        global_eval= reporting_io.write_global_evaluation(global_evaluation)
        
        reports = {'responses': responses,
                   'evaluations': evaluations,
                   'global_eval': global_eval
                   }
        
        return reports

class LangBiTe(AbstractLangBiTe):

    def __init__(self, prompts_path=None, file=None, file_dict=None):
        
        self.__prompts_path = dict()
        self.prompt_io = CSVPromptIOManager()
        super().__init__(file=file, file_dict=file_dict)
        if not prompts_path:
            self.__prompts_path['en_us'] = files('langbite.resources').joinpath('prompts_en_us.csv')
            self.__prompts_path['es_es'] = files('langbite.resources').joinpath('prompts_es_es.csv')
            self.__prompts_path['ca_es'] = files('langbite.resources').joinpath('prompts_ca_es.csv')
        else:
            self.__prompts_path = prompts_path
    
    def load_prompts(self):
        return self.prompt_io.load_prompts(self.__prompts_path, self._AbstractLangBiTe__test_scenario.languages)
    

class LangBiTeForAPI(AbstractLangBiTe):
    
    def __init__(self, json_data):
        file_dict = json_data['config']
        self.prompts = json_data['prompts']
        self.input_lang = json_data['input_language']
        self.prompt_io = JSONPromptIOManager()
        super().__init__(file_dict=file_dict)
  
    def load_prompts(self):
        return self.prompt_io.load_prompts(self.prompts, self.input_lang)
    