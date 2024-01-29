from langbite.oracle import ExpectedValueOracle, SameValueOracle

class OracleFactory:
    def __init__(self):
        self._builders = {}

    def register_builder(self, key, builder):
        self._builders[key] = builder

    def create(self, key, **kwargs):
        builder = self._builders.get(key)
        if not builder:
            raise ValueError(key)
        return builder(**kwargs)

class OracleBuilder:
    def __init__(self):
        pass

class ExpectedValueOracleBuilder(OracleBuilder):
    def __call__(self, prediction, prompt_id, **_ignored):
        self._instance = ExpectedValueOracle(prediction, prompt_id)
        return self._instance

class SameValueOracleBuilder(OracleBuilder):
    def __call__(self, prediction, prompt_id, **_ignored):
        self._instance = SameValueOracle(prediction, prompt_id)
        return self._instance

# class SentimentAnalyzerOracleBuilder(OracleBuilder):
#     def __call__(self, *config, **_ignored):
#         self._instance = SentimentAnalyzerOracle(config)
#         return self._instance

factory = OracleFactory()
factory.register_builder('expected value', ExpectedValueOracleBuilder())
factory.register_builder('same value', SameValueOracleBuilder())
#factory.register_builder('sentiment analyzer', SentimentAnalyzerOracleBuilder())