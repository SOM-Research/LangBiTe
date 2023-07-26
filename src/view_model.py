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

    _provider = None
    _model = None
    _concern = None
    _type = None
    _assessment = None
    _template = None
    _oracle_evaluation = None
    _oracle_prediction = None
    _evaluation = None

    @property
    def provider(self):
        return self._provider
    
    @property
    def model(self):
        return self._model
    
    @property
    def concern(self):
        return self._concern
    
    @property
    def type(self):
        return self._type
    
    @property
    def assessment(self):
        return self._assessment
    
    @property
    def template(self):
        return self._template
    
    @property
    def oracle_evaluation(self):
        return self._oracle_evaluation
    
    @property
    def oracle_prediction(self):
        return self._oracle_prediction
    
    @property
    def evaluation(self):
        return self._evaluation
    
    def __init__(self, provider, model, concern, type, assessment, template, oracle_evaluation, oracle_prediction, evaluation):
        self._provider = provider
        self._model = model
        self._concern = concern
        self._type = type
        self._assessment = assessment
        self._template = template
        self._oracle_evaluation = oracle_evaluation
        self._oracle_prediction = oracle_prediction
        self._evaluation = evaluation
    
    def to_dict(self):
        return {
            'Provider': self.provider,
            'Model': self.model,
            'Concern': self.concern,
            'Type': self.type,
            'Assessment': self.assessment,
            'Template': self.template,
            'Oracle Evaluation': self.oracle_evaluation,
            'Oracle Prediction': self.oracle_prediction,
            'Evaluation': self.evaluation
        }