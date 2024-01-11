import jsonschema


class OraclePredictionSchema:

    _schema = {
        'anyOf': [
            {
                'prediction_expected_value': {
                    'type': 'object',
                    'properties': {
                        'operation': {
                            'type': 'string',
                            'enum': ['equal', 'different', 'notIncludesAny', 'allEqualExpected']
                        },
                        'expected_value': {
                            'type': 'string'
                        }
                    },
                    'required': ['operation', 'expected_value']
                }
            },
            {
                'prediction_same_value': {
                    'type': 'object',
                    'properties': {
                        'operation': {
                            'type': 'string',
                            'enum': ['allSameValue']
                        },
                        'key': {
                            'type': 'string'
                        },
                        'delta': {
                            'type': 'number',
                            'minimum': 0,
                            'maximum': 100
                        }
                    },
                    'required': ['operation', 'key']
                }
            }
        ]
    }

    def __init__(self, prediction):
        self._prediction = prediction

    def validatePrediction(self) -> bool:
        try:
            jsonschema.validate(instance=self._prediction, schema=self._schema)
            return True
        except jsonschema.SchemaError as err:
            return False
        except jsonschema.ValidationError as err:
            return False
        except:
            return False