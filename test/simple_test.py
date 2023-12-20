# --- -------------------------------------------------------------------
# --- SIMPLE TEST
# ---
# --- Example of testing gender bias on OpenAI's GPT 3.5 turbo
# --- -------------------------------------------------------------------

import sys
import os
sys.path.insert(1, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src')))

from scenario_io_manager import ScenarioIOManager
from prompt_io_manager import PromptIOManager
from reporting_io_manager import ReportingIOManager
from global_evaluation import GlobalEvaluator
from test_scenario import TestScenario
from test_execution import TestExecution
from prompt import Prompt
from datetime import datetime


class SimpleTest:

    __file = 'simple_test.json'

    def __update_figures(self):
        self.__num_prompts = len(self.__test_scenario.prompts)
        self.__num_instances = 0
        prompt: Prompt
        for prompt in self.__test_scenario.prompts:
            self.__num_instances = self.__num_instances + len(prompt.instances)

    def generate(self):
        # load test scenario
        scenario_io = ScenarioIOManager()
        self.__test_scenario = TestScenario(scenario_io.load_scenario(self.__file))
        prompt_io = PromptIOManager()
        # test generation
        self.__test_scenario.prompts = prompt_io.load_prompts()
        # aux: for output reasons
        self.__update_figures()
    
    def execute(self):
        time_ini = datetime.now()
        # test execution and evaluation
        transaction = TestExecution(self.__test_scenario)
        transaction.execute_scenario()
        self.__responses = transaction.responses
        self.__evaluations = transaction.evaluations
        time_end = datetime.now()
        print(f'Time elapsed for executing {self.__num_instances} instances (from {self.__num_prompts} prompt templates): ' + str(time_end - time_ini))

    def report(self):
        global_evaluator = GlobalEvaluator()
        global_evaluation = global_evaluator.evaluate(self.__evaluations, self.__test_scenario.ethical_requirements)
        reporting_io = ReportingIOManager()
        reporting_io.write_responses(self.__responses)
        reporting_io.write_evaluations(self.__evaluations)
        reporting_io.write_global_evaluation(global_evaluation)

