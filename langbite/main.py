from langbite.LangBiTe import LangBiTe

test = LangBiTe(file='inputs/json-test-scenario.json')
test.generate()
test.execute()
test.report()


# from scenario_io_manager import ScenarioIOManager
# from prompt_io_manager import PromptIOManager
# from reporting_io_manager import ReportingIOManager
# from global_evaluation import GlobalEvaluator
# from test_scenario import TestScenario
# from test_execution import TestExecution
# from prompt import Prompt
# from datetime import datetime


# # -----------------------------------------------------------------------
# # main
# # -----------------------------------------------------------------------

# # TEST SCENARIO

# scenario_io = ScenarioIOManager()
# test_scenario = TestScenario(scenario_io.load_scenario('inputs/json-test-scenario.json'))

# # TEST GENERATION

# prompt_io = PromptIOManager()
# test_scenario.prompts = prompt_io.load_prompts()

# test_prompts = test_scenario.prompts
# num_instances = 0
# prompt: Prompt
# for prompt in test_prompts:
#     num_instances = num_instances + len(prompt.instances)

# # TEST EXECUTION AND EVALUATION

# time_ini = datetime.now()

# transaction = TestExecution(test_scenario)
# transaction.execute_scenario()
# responses = transaction.responses
# evaluations = transaction.evaluations

# time_end = datetime.now()

# print(f'Time elapsed for executing {num_instances} instances (from {len(test_prompts)} prompt templates): ' + str(time_end - time_ini))

# # TEST REPORTING

# global_evaluator = GlobalEvaluator()
# global_evaluation = global_evaluator.evaluate(evaluations, test_scenario.ethical_requirements)

# reporting_io = ReportingIOManager()
# reporting_io.write_responses(responses)
# reporting_io.write_evaluations(evaluations)
# reporting_io.write_global_evaluation(global_evaluation)