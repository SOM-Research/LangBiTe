import os
import importlib
import inspect

script_dir = os.path.dirname(os.path.abspath(__file__))

PLUGINS_PATH = f'{script_dir}/plugins'
MODULES_PATH = 'langbite.llm_services.plugins'

class PluginsImporter:
        
    def __init__(self):
        self.plugins_path = PLUGINS_PATH
    
    def import_all_plugins(self):
        imported_classes = {}

        for filename in os.listdir(self.plugins_path):
            if filename.endswith("factory.py") and filename != "__init__.py":
                module_name = filename[:-3]  # Remove .py extension
                module_path = f"{MODULES_PATH}.{module_name}"

                # Dynamically import the module
                module = importlib.import_module(module_path)

                # Get all classes in the module
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    try:
                        if inspect.isclass(obj):
                            imported_classes[name] = obj()  # Instantiate the builder class
                    except TypeError:
                        continue

        return imported_classes
