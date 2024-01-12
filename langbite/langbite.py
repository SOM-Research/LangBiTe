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

from langbite.scenario_io_manager import ScenarioIOManager
from langbite.prompt_io_manager import PromptIOManager
from langbite.reporting_io_manager import ReportingIOManager
from langbite.global_evaluation import GlobalEvaluator
from langbite.test_scenario import TestScenario
from langbite.test_execution import TestExecution
from langbite.prompt import Prompt
from datetime import datetime


class RequirementsFileRequiredException(Exception):
    '''Sorry, you must provide a requirements file name.'''

class WrongStateException(Exception):
    '''Sorry, you haven't followed the expected workflow. The proper invoking sequence is: init LangBite, generate, execute and report.'''

class LangBite:

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
    def requirements_file(self, value):
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

    # ---------------------------------------------------------------------------------
    # Internal and auxiliary methods
    # ---------------------------------------------------------------------------------

    def __init__(self, file=None, file_dict=None):
        self.requirements_file = file
        self.requirements_dict = file_dict
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
        self.generate
        self.execute
        self.report

    def generate(self):
        if (self.__current_status != 0): raise WrongStateException
        if (self.__requirements_file_empty): raise RequirementsFileRequiredException
        # load test scenario
        scenario_io = ScenarioIOManager()
        if self.requirements_file:
            self.__test_scenario = TestScenario(scenario_io.load_scenario(self.requirements_file))
        elif self.requirements_dict:
            self.__test_scenario = TestScenario(self.requirements_dict)
        prompt_io = PromptIOManager()
        # test generation
        self.__test_scenario.prompts = prompt_io.load_prompts()
        # aux: for output reasons
        self.__update_figures()
        self.__current_status = 1
    
    def execute(self):
        if (self.__current_status != 1): raise WrongStateException
        time_ini = datetime.now()
        # test execution and evaluation
        transaction = TestExecution(self.__test_scenario)
        transaction.execute_scenario()
        self.__responses = transaction.responses
        self.__evaluations = transaction.evaluations
        time_end = datetime.now()
        print(f'Time elapsed for executing {self.__num_instances} instances (from {self.__num_prompts} prompt templates): ' + str(time_end - time_ini))
        self.__current_status = 2

    def report(self):
        if (self.__current_status != 2): raise WrongStateException
        global_evaluator = GlobalEvaluator()
        global_evaluation = global_evaluator.evaluate(self.__evaluations, self.__test_scenario.ethical_requirements)
        reporting_io = ReportingIOManager()
        reporting_io.write_responses(self.__responses)
        reporting_io.write_evaluations(self.__evaluations)
        reporting_io.write_global_evaluation(global_evaluation)

