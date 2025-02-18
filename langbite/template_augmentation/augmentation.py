class AugmentationPair:

    @property
    def markup(self):
        return self.__markup
    
    @markup.setter
    def markup(self, value):
        self.__markup = value
    
    @property
    def communities(self):
        return self.__communities
    
    @communities.setter
    def communities(self, value):
        self.__communities = value

    @property
    def scenarios(self):
        return self.__scenarios
    
    @scenarios.setter
    def scenarios(self, value):
        self.__scenarios = value

    def __init__(self, context, concern):#, num_templates, language, llm):
        self.context = context
        self.concern = concern
        #self.num_templates = num_templates
        #self.language = language
        #self.llm = llm

class EthicalConcern:

    def __init__(self, concern, markup, communities):
        self.concern = concern
        self.markup = markup
        self.communities = communities

class Context:

    def __init__(self, context, scenarios):
        self.context = context
        self.scenarios = scenarios

class Augmentation:

    @property
    def augmentations(self) -> list[AugmentationPair]:
        return self.__augmentations
    
    @augmentations.setter
    def augmentations(self, value: list[AugmentationPair]):
        self.__augmentations = value

    def __init__(self, language, llm, num_templates, **ignore):
        self.language = language
        self.llm = llm
        self.num_templates = num_templates
        self.__augmentations = []
    
    def add_augmentation(self, value: AugmentationPair):
        self.__augmentations.append(value)