import langbite.utils

class EthicalRequirements:

    @property
    def requirements(self):
        return self.__requirements

    def __init__(self, requirements_json):
        self.__requirements = [EthicalRequirement(req) for req in requirements_json]

class EthicalRequirement:

    name: str
    rationale: str
    languages: list[str]
    tolerance: float
    delta: float
    concern: str
    communities: list[str]
    inputs: list[str]
    reflections: list[str]

    def __init__(self, req):
        self.name = req['name']
        self.rationale = req['rationale']
        self.languages = langbite.utils.lower_string_list(req['languages'])
        self.tolerance = req['tolerance']
        self.delta = req['delta']
        self.concern = req['concern'].lower()
        self.communities = langbite.utils.lower_string_list(req['communities'])
        self.inputs = langbite.utils.lower_string_list(req['inputs'])
        self.reflections = langbite.utils.lower_string_list(req['reflections'])