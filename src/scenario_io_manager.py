import random
import pandas
import json


class ScenarioIOManager:

    def load_scenario(self):
        # reads a json file containing the test scenario and
        # the ethical requirements model,
        # which are compliant with EthicsML
        f = open('inputs/json-test-scenario.json')
        return json.load(f)