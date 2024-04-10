import pandas as pd
from langbite.view_model import EvaluationView


class GlobalEvaluation:

    __provider = None
    __model = None
    __concern = None
    __input_type = None
    __reflection_type = None
    __passednr = 0
    __failednr = 0
    __errornr = 0
    __tolerance = None

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
    def input_type(self):
        return self.__input_type
    
    @property
    def reflection_type(self):
        return self.__reflection_type
    
    @property
    def passednr(self):
        return self.__passednr
    
    @property
    def failednr(self):
        return self.__failednr
    
    @property
    def errornr(self):
        return self.__errornr
    
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
    
    @property
    def tolerance(self):
        return self.__tolerance
    
    @property
    def tolerance_evaluation(self):
        return self.__tolerance_evaluation
    
    def __init__(self, provider, model, concern, input_type, reflection_type, passednr, failednr, errornr, tolerance, tolerance_evaluation):
        self.__provider = provider
        self.__model = model
        self.__concern = concern
        self.__input_type = input_type
        self.__reflection_type = reflection_type
        self.__passednr = passednr
        self.__failednr = failednr
        self.__errornr = errornr
        self.__tolerance = tolerance
        self.__tolerance_evaluation = tolerance_evaluation
    
    def to_dict(self):
        return {
            'Provider': self.provider,
            'Model': self.model,
            'Concern': self.concern,
            'Input Type': self.input_type,
            'Reflection Type': self.reflection_type,
            'Passed Nr': self.passednr,
            'Failed Nr': self.failednr,
            'Error Nr': self.errornr,
            'Passed Pct': self.passedpct,
            'Failed Pct': self.failedpct,
            'Total': self.total,
            'Tolerance': self.tolerance,
            'Tolerance Evaluation': self.tolerance_evaluation
        }

class GlobalEvaluator:

    def evaluate(self, evaluations: list[EvaluationView], ethical_requirements: list):
        df = pd.DataFrame.from_records([e.to_dict() for e in evaluations])
        df = df.groupby(by=['Provider','Model','Concern','Input Type','Reflection Type']).agg(**{
                'PassedNr': ('Evaluation', lambda s: s.eq('Passed').sum()),
                'FailedNr': ('Evaluation', lambda s: s.eq('Failed').sum()),
                'ErrorNr': ('Evaluation', lambda s: s.eq('Error').sum())
           }).reset_index()
        self.__evaluate_tolerance(df, ethical_requirements)
        return self.__evaluations_tolist(df)
    
    def __evaluate_tolerance(self, df: pd.DataFrame, ethical_requirements: list):
        tolerances = {req.concern:req.tolerance for req in ethical_requirements}
        df['Tolerance'] = df.apply(lambda row: tolerances[row.Concern], axis=1)
        df['Tolerance Evaluation'] = df.apply(lambda row: self.__evaluate(tolerances[row.Concern], row.PassedNr, row.FailedNr), axis=1)
    
    def __evaluate(self, tolerance, passednr, failednr) -> str:
        if ((passednr + failednr) == 0): return 'Not evaluated'
        if (tolerance <= (passednr / (passednr + failednr))): return 'Passed'
        return 'Failed'
    
    def __evaluations_tolist(self, df: pd.DataFrame) -> list:
        if df is None: return []
        return list(map(lambda x:GlobalEvaluation(
            provider=x[0],
            model=x[1],
            concern=x[2],
            input_type=x[3],
            reflection_type=x[4],
            passednr=x[5],
            failednr=x[6],
            errornr=x[7],
            tolerance=x[8],
            tolerance_evaluation=x[9]
        ),df.values.tolist()))