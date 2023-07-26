import pandas as pd
from view_model import EvaluationView


class GlobalEvaluation:

    _provider = None
    _model = None
    _concern = None
    _type = None
    _assessment = None
    _passednr = 0
    _failednr = 0
    _total = 0

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
    def passednr(self):
        return self._passednr
    
    @property
    def failednr(self):
        return self._failednr
    
    @property
    def passedpct(self):
        if (self.total == 0): return 0
        return self.passednr / self.total
    
    @property
    def failedpct(self):
        if (self.total == 0): return 0
        return self.failednr / self.total
    
    @property
    def total(self):
        return self.passednr + self.failednr
    
    def __init__(self, provider, model, concern, type, assessment, passednr, failednr):
        self._provider = provider
        self._model = model
        self._concern = concern
        self._type = type
        self._assessment = assessment
        self._passednr = passednr
        self._failednr = failednr
    
    def to_dict(self):
        return {
            'Provider': self.provider,
            'Model': self.model,
            'Concern': self.concern,
            'Type': self.type,
            'Assessment': self.assessment,
            'Passed Nr': self.passednr,
            'Failed Nr': self.failednr,
            'Passed Pct': self.passedpct,
            'Failed Pct': self.failedpct,
            'Total': self.total
        }

class GlobalEvaluator:

    def evaluate(self, evaluations: list[EvaluationView]):
        df = pd.DataFrame.from_records([e.to_dict() for e in evaluations])
        df = df.groupby(by=['Provider','Model','Concern','Type','Assessment']).agg(**{
                'Passed Nr': ('Evaluation', lambda s: s.eq('Passed').sum()),
                'Failed Nr': ('Evaluation', lambda s: s.eq('Failed').sum())
           }).reset_index()
        print(df)
        return list(map(lambda x:GlobalEvaluation(
            provider=x[0],
            model=x[1],
            concern=x[2],
            type=x[3],
            assessment=x[4],
            passednr=x[5],
            failednr=x[6]
        ),df.values.tolist()))