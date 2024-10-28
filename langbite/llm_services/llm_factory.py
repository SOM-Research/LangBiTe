from langbite.llm_services.llm_abstract_factory import LLMFactory
from langbite.llm_services.llm_huggingface_factory import HuggingFaceCompletionServiceBuilder, HuggingFaceConversationalServiceBuilder
from langbite.llm_services.llm_openai_factory import OpenAIChatServiceBuilder
from langbite.llm_services.llm_replicate_factory import ReplicateServiceBuilder
from langbite.llm_services.llm_plugins_factory import PluginsImporter

factory = LLMFactory()

plugins_importer = PluginsImporter()
plugins = plugins_importer.import_all_plugins()

# Register all plugins
for plugin_name, builder in plugins.items():
    if hasattr(builder, 'name'):  # Check if the method exists
        factory.register_builder(builder.name(), builder) 

    
# HuggingFace's text completion models

# factory.register_builder('HuggingFaceGPT2', HuggingFaceCompletionServiceBuilder('https://api-inference.huggingface.co/models/gpt2'))
# factory.register_builder('HuggingFaceGPT2Large', HuggingFaceCompletionServiceBuilder('https://api-inference.huggingface.co/models/gpt2-large'))
# factory.register_builder('HuggingFaceGPT2XLarge', HuggingFaceCompletionServiceBuilder('https://api-inference.huggingface.co/models/gpt2-xl'))

# HuggingFace's conversational models

# factory.register_builder('HuggingFaceMicrosoftDialoGPTSmall', HuggingFaceConversationalServiceBuilder('https://api-inference.huggingface.co/models/microsoft/DialoGPT-small'))
# factory.register_builder('HuggingFaceMicrosoftDialoGPTLarge', HuggingFaceConversationalServiceBuilder('https://api-inference.huggingface.co/models/microsoft/DialoGPT-large'))
# factory.register_builder('HuggingFaceMicrosoftGodelLarge', HuggingFaceConversationalServiceBuilder('https://api-inference.huggingface.co/models/microsoft/GODEL-v1_1-large-seq2seq'))
# factory.register_builder('HuggingFaceMicrosoftPhi3Mini128K', HuggingFaceConversationalServiceBuilder('https://api-inference.huggingface.co/models/microsoft/Phi-3-mini-128k-instruct'))

# factory.register_builder('HuggingFaceFacebookBlenderBot400M', HuggingFaceConversationalServiceBuilder('https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill'))
# factory.register_builder('HuggingFaceFacebookBlenderBot1B', HuggingFaceConversationalServiceBuilder('https://api-inference.huggingface.co/models/facebook/blenderbot-1B-distill'))
# factory.register_builder('HuggingFaceFacebookBlenderBot3B', HuggingFaceConversationalServiceBuilder('https://api-inference.huggingface.co/models/facebook/blenderbot-3B'))

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

# these next two are for question answering, may require different invoke method
#factory.register_builder('HuggingFaceRobertaBaseSquad2', HuggingFaceQuestionAnsweringServiceBuilder('https://api-inference.huggingface.co/models/deepset/roberta-base-squad2'))
#factory.register_builder('HuggingFaceDistilbertBaseUncased', HuggingFaceQuestionAnsweringServiceBuilder('https://api-inference.huggingface.co/models/distilbert-base-uncased-distilled-squad'))

# OpenAI's chat models

factory.register_builder('OpenAIGPT35Turbo0613', OpenAIChatServiceBuilder('gpt-3.5-turbo-0613')) # snapshot June 13th 2023, deprecated June 13th 2024
factory.register_builder('OpenAIGPT35Turbo1106', OpenAIChatServiceBuilder('gpt-3.5-turbo-1106')) # snapshot November 6th 2023
factory.register_builder('OpenAIGPT40613', OpenAIChatServiceBuilder('gpt-4-0613')) # snapshot June 13th 2023
factory.register_builder('OpenAIGPT35Turbo', OpenAIChatServiceBuilder('gpt-3.5-turbo'))
# factory.register_builder('OpenAIGPT35Turbo16k', OpenAIChatServiceBuilder('gpt-3.5-turbo-16k')) # legacy
factory.register_builder('OpenAIGPT4', OpenAIChatServiceBuilder('gpt-4'))
factory.register_builder('OpenAIGPT4Turbo', OpenAIChatServiceBuilder('gpt-4-turbo'))
factory.register_builder('OpenAIGPT4o', OpenAIChatServiceBuilder('gpt-4o'))

factory.register_builder('OpenAIGPT35TurboInstruct', OpenAIChatServiceBuilder('gpt-3.5-turbo-instruct'))

# Replicate models

factory.register_builder('Llama27BChat', ReplicateServiceBuilder('meta/llama-2-7b-chat'))
factory.register_builder('Llama213BChat', ReplicateServiceBuilder('meta/llama-2-13b-chat'))
factory.register_builder('Llama270BChat', ReplicateServiceBuilder('meta/llama-2-70b-chat'))


# factory.register_builder('ModulosChat', ModulosChatServiceBuilder())
# ------------------------------------------------
# DEPRECATED MODELS
# ------------------------------------------------

# OpenAI's text completion models

# factory.register_builder('OpenAITextCurie001', OpenAIServiceBuilder('text-curie-001')) # deprecated on 2024-01-04
# factory.register_builder('OpenAITextBabbage001', OpenAIServiceBuilder('text-babbage-001')) # deprecated on 2024-01-04
# factory.register_builder('OpenAITextAda001', OpenAIServiceBuilder('text-ada-001')) # deprecated on 2024-01-04
# factory.register_builder('OpenAITextDaVinci003', OpenAIServiceBuilder('text-davinci-003')) # deprecated on 2024-01-04

# OpenAI's chat models

# factory.register_builder('OpenAIGPT35Turbo0301', OpenAIChatServiceBuilder('gpt-3.5-turbo-0301')) # snapshot March 1st, 2023 # deprecated on 2024-06-13
# factory.register_builder('OpenAIGPT35Turbo0613', OpenAIChatServiceBuilder('gpt-3.5-turbo-0613')) # snapshot June 13th, 2023 # deprecated on 2024-06-13
# factory.register_builder('OpenAIGPT40314', OpenAIChatServiceBuilder('gpt-4-0314')) # snapshot March 14th, 2023 # deprecated on 2024-06-13
