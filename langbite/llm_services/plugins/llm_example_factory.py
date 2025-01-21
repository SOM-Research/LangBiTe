from langbite.llm_services.plugins.llm_example_service import ExampleService

class ExampleServiceBuilder:
    def __init__(self):
        self._instance = None
    
    def __call__(self, **_ignored):
        if not self._instance:
            self._instance = ExampleService()
        return self._instance

    def name(self):
        return 'ExampleAI'