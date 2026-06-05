from langbite.llm_services.llm_abstract_factory import LLMFactory
from langbite.llm_services.llm_gpt4all_service import GPT4AllServiceBuilder
from langbite.llm_services.llm_huggingface_factory import HuggingFaceConversationalServiceBuilder
from langbite.llm_services.llm_openai_factory import OpenAIChatServiceBuilder
from langbite.llm_services.llm_replicate_service import ReplicateServiceBuilder
from langbite.llm_services.llm_ollama_factory import OLlamaServiceBuilder
import langbite.io_managers.json_io_manager as FactoriesIOManager
#from langbite.llm_services.llm_plugins_factory import PluginsImporter

factory = LLMFactory()

builders = FactoriesIOManager.load_factories()
for builder in builders:
    provider = builder['provider'].upper()
    if provider == 'OPENAI':
        factory.register_builder(builder['key'], OpenAIChatServiceBuilder(builder['model'].lower()))
    if provider == 'HUGGINGFACE':
        factory.register_builder(builder['key'], HuggingFaceConversationalServiceBuilder(builder['model'].lower(), builder['inference_api_url']))
    if provider == 'OLLAMA':
        factory.register_builder(builder['key'], OLlamaServiceBuilder(builder['model'].lower()))
    if provider == 'REPLICATE':
        factory.register_builder(builder['key'], ReplicateServiceBuilder(builder['model'].lower()))
    if provider == 'GPT4ALL':
        factory.register_builder(builder['key'], GPT4AllServiceBuilder())

# plugins_importer = PluginsImporter()
# plugins = plugins_importer.import_all_plugins()

# Register all plugins
# for plugin_name, builder in plugins.items():
#     if hasattr(builder, 'name'):  # Check if the method exists
#         factory.register_builder(builder.name(), builder) 

    
