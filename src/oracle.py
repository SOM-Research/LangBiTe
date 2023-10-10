from abc import abstractmethod
from enum import Enum
import json
import re
from oracle_prediction_validation import OraclePredictionSchema


ExpectedValueOperationKind = Enum('IndividualOperation', 'equal different notIncludesAny allEqualExpected')
SameValueOperationKind = Enum('GroupOperation', 'allSameValue')

OracleResultKind = Enum('OracleResult', 'Passed Failed Error')

class Oracle:

    _valid_operations = []

    @property
    def prompt_id(self):
        return self._prompt_id
    
    @property
    def is_valid_prediction(self) -> bool:
        return self._is_valid_prediction
    
    @is_valid_prediction.setter
    def is_valid_prediction(self, value):
        self._is_valid_prediction = value

    @property
    def expected_value(self) -> str:
        try: result = self._expected_value
        except: result = 'NONE'
        return result
    
    @expected_value.setter
    def expected_value(self, value):
        self._expected_value = self.clean(value)
    
    @property
    def operation(self) -> str:
        return self._operation
    
    @operation.setter
    def operation(self, value):
        self._operation = value

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        if value: self._result = OracleResultKind.Passed.name
        else: self._result = OracleResultKind.Failed.name

    def __init__(self, prediction, prompt_id, **kwargs):
        self._prompt_id = prompt_id
        self.setValidOperations()
        self._evaluators = dict(zip(self._valid_operations, self._valid_operations))
        opv = OraclePredictionSchema(prediction)
        self.is_valid_prediction = opv.validatePrediction()
        self.is_valid_prediction = True
        if (self.is_valid_prediction): self.initiateOperation(prediction)

    def initiateOperation(self, prediction):
        self._prediction = json.loads(prediction)
        self.operation = self._prediction['operation']
        self.initiateConcreteOperation()

    @abstractmethod
    def initiateConcreteOperation(self):
        pass

    @abstractmethod
    def setValidOperations(self):
        pass

    @abstractmethod
    def validateConcretePrediction(self) -> bool:
        pass

    def evaluate(self, responses: list[str]) -> OracleResultKind:
        if (not self.is_valid_prediction): return OracleResultKind.Error.name
        else: return self.evaluateConcrete(responses)

    @abstractmethod
    def evaluateConcrete(self, responses: list[str]) -> OracleResultKind:
        pass

    def clean(self, value: str) -> str:
        return re.sub('\n','',value.strip()).lower()
    
    def allEqualsToValue(self, list: list, value: str) -> bool:
        return all(self.valueEqualsToValue(item, value) for item in list)
    
    def valueEqualsToValue(self, value: str, expected: str) -> bool:
        cleaned_value = self.clean(value)
        cleaned_expected = self.clean(expected)
        return cleaned_value == cleaned_expected
    

class ExpectedValueOracle(Oracle):
    
    def setValidOperations(self):
        self._valid_operations = ExpectedValueOperationKind._member_names_

    def initiateConcreteOperation(self):
        self.expected_value = self._prediction['expected_value']

    def evaluateConcrete(self, responses):
        operation = self._evaluators[self.operation]
        evaluate_method = getattr(self, operation)
        if operation == ExpectedValueOperationKind.allEqualExpected.name: return evaluate_method(responses)
        else: return evaluate_method(responses[0])
    
    def equal(self, response):
        self.result = self.responseMatchesExpectedValue(response)
        return self.result
    
    def different(self, response):
        self.result = not self.responseMatchesExpectedValue(response)
        return self.result
    
    def responseMatchesExpectedValue(self, response: str) -> bool:
        return self.responseMatchesValue(response, self.expected_value)
    
    def responseMatchesValue(self, response: str, value: str) -> bool:
        cleaned_response = self.clean(response)
        p = re.compile(r'^\b' + value + r'\b', re.IGNORECASE)
        m = p.search(cleaned_response)
        if m: return True
        return False

    def notIncludesAny(self, response):
        exclude = self.expected_value.split()
        self.result = not any(self.responseMatchesValue(response, x) for x in exclude)
        return self.result

    def allEqualExpected(self, responses: list[str]):
        self.result = self.allEqualsToValue(responses, self.expected_value)
        return self.result


class SameValueOracle(Oracle):

    def setValidOperations(self):
        self._valid_operations = SameValueOperationKind._member_names_

    def initiateConcreteOperation(self):
        self.key = self._prediction['key']
        self.has_delta = 'delta' in self._prediction
        if (self.has_delta): self.delta = self._prediction['delta']

    def evaluateConcrete(self, responses):
        operation = self._evaluators[self.operation]
        evaluate_method = getattr(self, operation)
        return evaluate_method(responses)
    
    def allSameValue(self, responses):
        responses_key = [json.loads(response)[self.key] for response in responses]
        if (type(responses_key[0]) == int or float):
            if (not self.has_delta):
                self.result = all(response == responses_key[0] for response in responses_key)
            else:
                #numbers = np.array(responses_key)
                #mad = np.median(abs(numbers - np.median(numbers)))
                #self.result = mad <= self._delta
                max_value = max(responses_key)
                min_value = min(responses_key)
                self.result = (max_value - min_value) <= self.delta
        else: self.result = self.allEqualsToValue(responses_key, responses_key[0])
        return self.result
