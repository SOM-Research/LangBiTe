from langbite.llm_replicate_service import ReplicateService


class ReplicateServiceBuilder:
    def __init__(self, model):
        self._instance = None
        self._model = model

    def __call__(self, replicate_api_key, **_ignored):
        if not self._instance:
            self._instance = ReplicateService(replicate_api_key, self._model)
        return self._instance
