class ResponseView:

    _provider = None
    _model = None
    _instance = None
    _response = None

    @property
    def provider(self):
        return self._provider
    
    @property
    def model(self):
        return self._model
    
    @property
    def instance(self):
        return self._instance
    
    @property
    def response(self):
        return self._response
    
    def __init__(self, provider, model, instance, response):
        self._provider = provider
        self._model = model
        self._instance = instance
        self._response = response
    
    def to_dict(self):
        return {
            'Provider': self.provider,
            'Model': self.model,
            'Instance': self.instance,
            'Response': self.response
        }
    

class EvaluationView:

    __provider = None
    __model = None
    __concern = None
    __language = None
    __input_type = None
    __reflection_type = None
    __template = None
    __oracle_evaluation = None
    __oracle_prediction = None
    __evaluation = None

    @property
    def provider(self):
        return self.__provider
    
    @property
    def model(self):
        return self.__model
    
    @property
    def concern(self):
        return self.__concern
    
    @property
    def language(self):
        return self.__language
    
    @property
    def input_type(self):
        return self.__input_type
    
    @property
    def reflection_type(self):
        return self.__reflection_type
    
    @property
    def template(self):
        return self.__template
    
    @property
    def oracle_evaluation(self):
        return self.__oracle_evaluation
    
    @property
    def oracle_prediction(self):
        return self.__oracle_prediction
    
    @property
    def evaluation(self):
        return self.__evaluation
    
    def __init__(self, provider, model, concern, language, input_type, reflection_type, template, oracle_evaluation, oracle_prediction, evaluation):
        self.__provider = provider
        self.__model = model
        self.__concern = concern
        self.__language = language
        self.__input_type = input_type
        self.__reflection_type = reflection_type
        self.__template = template
        self.__oracle_evaluation = oracle_evaluation
        self.__oracle_prediction = oracle_prediction
        self.__evaluation = evaluation
    
    def to_dict(self):
        return {
            'Provider': self.provider,
            'Model': self.model,
            'Concern': self.concern,
            'Language': self.language,
            'Input Type': self.input_type,
            'Reflection Type': self.reflection_type,
            'Template': self.template,
            'Oracle Evaluation': self.oracle_evaluation,
            'Oracle Prediction': self.oracle_prediction,
            'Evaluation': self.evaluation
        }