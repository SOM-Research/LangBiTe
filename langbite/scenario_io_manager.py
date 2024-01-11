import json
import os
import sys


class ScenarioIOManager:

    def load_scenario(self, file):
        # reads a json file containing the test scenario and
        # the ethical requirements model,
        # which are compliant with EthicsML
        #path = os.path.normpath(os.path.join(sys.path[0], file))
        #f = open(path)
        f = open(file)
        return json.load(f)