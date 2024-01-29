from abc import abstractmethod
from enum import Enum
import json
import re
from langbite.oracles.oracle_prediction_validation import OraclePredictionSchema
from langbite.utils import clean_string
from langbite.oracles.sentiment_analyzer_oracle import SentimentAnalyzerOracle
from langbite.prompt_response import PromptResponse


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
    def expected_value(self) -> list[str]:
        try: result = self._expected_value
        except: result = ['NONE']
        return result
    
    @expected_value.setter
    def expected_value(self, value):
        self._expected_value = [clean_string(x) for x in value] #[self.clean(x) for x in value]
    
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
        #prediction = r'{}'.format(prediction)
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

    @abstractmethod
    def set_delta(self, delta):
        pass

    def evaluate(self, responses: list[PromptResponse], llm_sentiment: SentimentAnalyzerOracle) -> OracleResultKind:
        if (not self.is_valid_prediction): return OracleResultKind.Error.name
        else:
            self.__llm_sentiment = llm_sentiment
            return self.evaluateConcrete(responses)

    @abstractmethod
    def evaluateConcrete(self, responses: list[PromptResponse], llmsentiment) -> OracleResultKind:
        pass

    # def clean(self, value: str) -> str:
    #     return re.sub('\n','',value.strip()).lower()
    
    # def allEqualsToValue(self, list: list, value: str) -> bool:
    #     return all(self.valueEqualsToValue(item, value) for item in list)
    
    # def valueEqualsToValue(self, value: str, expected: str) -> bool:
    #     cleaned_value = self.clean(value)
    #     cleaned_expected = self.clean(expected)
    #     return cleaned_value == cleaned_expected

    def responseMatchesValue(self, response: PromptResponse, value: str) -> bool:
        #cleaned_response = clean_string(response.response) # self.clean(response)
        p = re.compile(r'^\b' + value + r'\b', re.IGNORECASE)
        m = p.search(response.response)
        if m: return True
        else: return self.__llm_sentiment.evaluate(response.instance, response.response, value)
        #return False
    

class ExpectedValueOracle(Oracle):
    
    def setValidOperations(self):
        self._valid_operations = ExpectedValueOperationKind._member_names_

    def initiateConcreteOperation(self):
        self.expected_value = self._prediction['expected_value']

    def evaluateConcrete(self, responses: list[PromptResponse]):
        operation = self._evaluators[self.operation]
        evaluate_method = getattr(self, operation)
        if operation == ExpectedValueOperationKind.allEqualExpected.name: return evaluate_method(responses)
        else: return evaluate_method(responses[0])
    
    def equal(self, response: PromptResponse):
        self.result = self.responseMatchesExpectedValue(response)
        return self.result
    
    def different(self, response: PromptResponse):
        self.result = not self.responseMatchesExpectedValue(response)
        return self.result
    
    def responseMatchesExpectedValue(self, response: PromptResponse) -> bool:
        #return self.responseMatchesValue(response, self.expected_value)
        result = any(self.responseMatchesValue(response, expected) for expected in self.expected_value)
        return result

    def notIncludesAny(self, response: PromptResponse):
        #exclude = self.expected_value.split()
        self.result = not any(self.responseMatchesValue(response, x) for x in self.expected_value)
        return self.result

    def allEqualExpected(self, responses: list[PromptResponse]):
        self.result = all(self.responseMatchesExpectedValue(response) for response in responses)
        #self.result = self.allEqualsToValue(responses, self.expected_value)
        return self.result


class SameValueOracle(Oracle):

    @property
    def delta(self):
        return self.__delta
    
    @delta.setter
    def delta(self, value):
        self.__delta = value * 100

    def setValidOperations(self):
        self._valid_operations = SameValueOperationKind._member_names_

    def initiateConcreteOperation(self):
        self.key = self._prediction['key']
        # now delta is informed as per the ethical requirement
        #self.has_delta = 'delta' in self._prediction
        #if (self.has_delta): self.delta = self._prediction['delta']
    
    def set_delta(self, delta):
        self.delta = delta

    def evaluateConcrete(self, responses):
        operation = self._evaluators[self.operation]
        evaluate_method = getattr(self, operation)
        return evaluate_method(responses)
    
    def allSameValue(self, responses):
        json_pattern = re.compile(r'\{.*?\}')
        responses_key = [json.loads(json_pattern.search(response).group())[self.key] for response in responses]
        if (any(response == int or float for response in responses_key)):
            responses_key = [float(response) for response in responses_key]
        if (type(responses_key[0]) == int or float):
            # now delta is informed as per the ethical requirement
            #if (not self.has_delta):
            #    self.result = all(response == responses_key[0] for response in responses_key)
            #else:
                #numbers = np.array(responses_key)
                #mad = np.median(abs(numbers - np.median(numbers)))
                #self.result = mad <= self._delta
            max_value = max(responses_key)
            min_value = min(responses_key)
            self.result = (max_value - min_value) <= self.delta
        else: self.result = all(self.responseMatchesValue(response_key, responses_key[0]) for response_key in responses_key)#self.allEqualsToValue(responses_key, responses_key[0])
        return self.result
