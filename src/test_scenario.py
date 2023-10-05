import json


class TestScenario:

    def __init__(self, cfg):
        #cfg_json = json.loads(cfg)
        self._timestamp = cfg['timestamp']
        self._temperature = cfg['temperature']
        self._tokens = cfg['tokens']
        self._ethical_requirements = cfg['requirements']