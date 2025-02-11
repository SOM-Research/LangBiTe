class Augmentation:

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

    def __init__(self, context, concern, num_templates, languages): #, llm):
        self.context = context
        self.concern = concern
        self.num_templates = num_templates
        self.languages = languages
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

