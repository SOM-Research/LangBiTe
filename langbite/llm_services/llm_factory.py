from langbite.llm_services.llm_abstract_factory import LLMFactory
from langbite.llm_services.llm_huggingface_factory import HuggingFaceConversationalServiceBuilder
from langbite.llm_services.llm_openai_factory import OpenAIChatServiceBuilder
from langbite.llm_services.llm_replicate_service import ReplicateServiceBuilder
from langbite.llm_services.llm_ollama_factory import OLlamaServiceBuilder
from langbite.llm_services.llm_plugins_factory import PluginsImporter

factory = LLMFactory()


factory = LLMFactory()

plugins_importer = PluginsImporter()
plugins = plugins_importer.import_all_plugins()

# Register all plugins
for plugin_name, builder in plugins.items():
    if hasattr(builder, 'name'):  # Check if the method exists
        factory.register_builder(builder.name(), builder) 

    
# HuggingFace's conversational models


factory.register_builder('HuggingFaceFlanT5Base', HuggingFaceConversationalServiceBuilder('https://api-inference.huggingface.co/models/google/flan-t5-base'))
factory.register_builder('HuggingFaceFlanT5Large', HuggingFaceConversationalServiceBuilder('https://api-inference.huggingface.co/models/google/flan-t5-large'))
factory.register_builder('HuggingFaceFlanT5XXL', HuggingFaceConversationalServiceBuilder('https://api-inference.huggingface.co/models/google/flan-t5-xxl'))

factory.register_builder('HuggingFaceMT5Base', HuggingFaceConversationalServiceBuilder('https://api-inference.huggingface.co/models/google/mt5-base'))
factory.register_builder('HuggingFaceMT5Large', HuggingFaceConversationalServiceBuilder('https://api-inference.huggingface.co/models/google/mt5-large'))

factory.register_builder('HuggingFaceGemma2BIT', HuggingFaceConversationalServiceBuilder('https://api-inference.huggingface.co/models/google/gemma-2b-it'))

factory.register_builder('HuggingFaceMistral7B02Instruct', HuggingFaceConversationalServiceBuilder('https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2'))
factory.register_builder('HuggingFaceMistral7B01', HuggingFaceConversationalServiceBuilder('https://api-inference.huggingface.co/models/mistralai/Mistral-7B-v0.1'))
factory.register_builder('HuggingFaceMixtral8x7B01Instruct', HuggingFaceConversationalServiceBuilder('https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1'))

factory.register_builder('HuggingFaceFalcon7BInstruct', HuggingFaceConversationalServiceBuilder('https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct'))

factory.register_builder('HuggingFaceLlama318BInstruct', HuggingFaceConversationalServiceBuilder('https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3.1-8B-Instruct'))


# OpenAI's chat models

factory.register_builder('OpenAIGPT35Turbo0613', OpenAIChatServiceBuilder('gpt-3.5-turbo-0613')) # snapshot June 13th 2023, deprecated June 13th 2024
factory.register_builder('OpenAIGPT35Turbo1106', OpenAIChatServiceBuilder('gpt-3.5-turbo-1106')) # snapshot November 6th 2023
factory.register_builder('OpenAIGPT40613', OpenAIChatServiceBuilder('gpt-4-0613')) # snapshot June 13th 2023
factory.register_builder('OpenAIGPT35Turbo', OpenAIChatServiceBuilder('gpt-3.5-turbo'))
factory.register_builder('OpenAIGPT4', OpenAIChatServiceBuilder('gpt-4'))
factory.register_builder('OpenAIGPT4Turbo', OpenAIChatServiceBuilder('gpt-4-turbo'))
factory.register_builder('OpenAIGPT4o', OpenAIChatServiceBuilder('gpt-4o'))

factory.register_builder('OpenAIGPT35TurboInstruct', OpenAIChatServiceBuilder('gpt-3.5-turbo-instruct'))

# Replicate models

factory.register_builder('Llama27BChat', ReplicateServiceBuilder('meta/llama-2-7b-chat'))
factory.register_builder('Llama213BChat', ReplicateServiceBuilder('meta/llama-2-13b-chat'))
factory.register_builder('Llama270BChat', ReplicateServiceBuilder('meta/llama-2-70b-chat'))

# Models hosted in OLlama server

factory.register_builder('OLlamaSalamandra2BInstruct', OLlamaServiceBuilder('BSC-LT/salamandra-2b-instruct'))
factory.register_builder('OLlamaMistral', OLlamaServiceBuilder('mistral'))

