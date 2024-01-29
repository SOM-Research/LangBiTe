class OraclePrediction:

    @property
    def is_valid(self):
        return self._is_valid
    
    @property
    def operation(self):
        return self._operation
    
    def __init__(self):
        self._is_valid = False

class OracleIndividualBooleanPrediction(OraclePrediction):

    @property
    def expected_value(self):
        return self._expected_value
    
    @expected_value.setter
    def expected_value(self, value):
        self._expected_value = value

class OracleIndividualGroupPrediction(OraclePrediction):

    @property
    def key(self):
        return self._key
    
    @key.setter
    def key(self, value):
        self._key = value
    
    @property
    def delta(self):
        return self._delta
    
    @key.setter
    def delta(self, value):
        if (type(value) == int or float):
            self._delta = value

    @property
    def has_delta(self):
        return self.delta is not None