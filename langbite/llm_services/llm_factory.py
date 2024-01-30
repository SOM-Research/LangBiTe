from langbite.llm_services.llm_abstract_factory import LLMFactory
from langbite.llm_services.llm_huggingface_factory import HuggingFaceCompletionServiceBuilder, HuggingFaceConversationalServiceBuilder #HuggingFaceQuestionAnsweringServiceBuilder
from langbite.llm_services.llm_openai_factory import OpenAIChatServiceBuilder, OpenAIServiceBuilder
from langbite.llm_services.llm_replicate_factory import ReplicateServiceBuilder

factory = LLMFactory()

# HuggingFace's text completion models

factory.register_builder('HuggingFaceGPT2', HuggingFaceCompletionServiceBuilder('https://api-inference.huggingface.co/models/gpt2'))
factory.register_builder('HuggingFaceGPT2Large', HuggingFaceCompletionServiceBuilder('https://api-inference.huggingface.co/models/gpt2-large'))
factory.register_builder('HuggingFaceGPT2XLarge', HuggingFaceCompletionServiceBuilder('https://api-inference.huggingface.co/models/gpt2-xl'))

factory.register_builder('HuggingFaceMistral7B', HuggingFaceCompletionServiceBuilder('https://api-inference.huggingface.co/models/mistralai/Mistral-7B-v0.1'))

# HuggingFace's conversational models

factory.register_builder('HuggingFaceMicrosoftDialoGPTSmall', HuggingFaceConversationalServiceBuilder('https://api-inference.huggingface.co/models/microsoft/DialoGPT-small'))
factory.register_builder('HuggingFaceMicrosoftDialoGPTLarge', HuggingFaceConversationalServiceBuilder('https://api-inference.huggingface.co/models/microsoft/DialoGPT-large'))
factory.register_builder('HuggingFaceMicrosoftGodelLarge', HuggingFaceConversationalServiceBuilder('https://api-inference.huggingface.co/models/microsoft/GODEL-v1_1-large-seq2seq'))

factory.register_builder('HuggingFaceFacebookBlenderBot400M', HuggingFaceConversationalServiceBuilder('https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill'))
factory.register_builder('HuggingFaceFacebookBlenderBot1B', HuggingFaceConversationalServiceBuilder('https://api-inference.huggingface.co/models/facebook/blenderbot-1B-distill'))
factory.register_builder('HuggingFaceFacebookBlenderBot3B', HuggingFaceConversationalServiceBuilder('https://api-inference.huggingface.co/models/facebook/blenderbot-3B'))

# these next two are for question answering, may require different invoke method
#factory.register_builder('HuggingFaceRobertaBaseSquad2', HuggingFaceQuestionAnsweringServiceBuilder('https://api-inference.huggingface.co/models/deepset/roberta-base-squad2'))
#factory.register_builder('HuggingFaceDistilbertBaseUncased', HuggingFaceQuestionAnsweringServiceBuilder('https://api-inference.huggingface.co/models/distilbert-base-uncased-distilled-squad'))

# OpenAI's text completion models

# factory.register_builder('OpenAITextCurie001', OpenAIServiceBuilder('text-curie-001')) # deprecated on 2024-01-04
# factory.register_builder('OpenAITextBabbage001', OpenAIServiceBuilder('text-babbage-001')) # deprecated on 2024-01-04
# factory.register_builder('OpenAITextAda001', OpenAIServiceBuilder('text-ada-001')) # deprecated on 2024-01-04
# factory.register_builder('OpenAITextDaVinci003', OpenAIServiceBuilder('text-davinci-003')) # deprecated on 2024-01-04

# OpenAI's chat models

factory.register_builder('OpenAIGPT35Turbo0301', OpenAIChatServiceBuilder('gpt-3.5-turbo-0301')) # snapshot March 1st, 2023
# factory.register_builder('OpenAIGPT35Turbo0613', OpenAIChatServiceBuilder('gpt-3.5-turbo-0613')) # snapshot June 13th, 2023 # deprecated on 2024-06-13
factory.register_builder('OpenAIGPT35Turbo0613', OpenAIChatServiceBuilder('gpt-3.5-turbo-1106')) # snapshot November 6th, 2023
# factory.register_builder('OpenAIGPT40314', OpenAIChatServiceBuilder('gpt-4-0314')) # snapshot March 14th, 2023 # deprecated on 2024-06-13
factory.register_builder('OpenAIGPT40613', OpenAIChatServiceBuilder('gpt-4-0613')) # snapshot June 13th, 2023
factory.register_builder('OpenAIGPT35Turbo', OpenAIChatServiceBuilder('gpt-3.5-turbo'))
factory.register_builder('OpenAIGPT35Turbo16k', OpenAIChatServiceBuilder('gpt-3.5-turbo-16k'))
factory.register_builder('OpenAIGPT4', OpenAIChatServiceBuilder('gpt-4'))

# Replicate models

factory.register_builder('Llama27BChat', ReplicateServiceBuilder('meta/llama-2-7b-chat'))
factory.register_builder('Llama213BChat', ReplicateServiceBuilder('meta/llama-2-13b-chat'))
factory.register_builder('Llama270BChat', ReplicateServiceBuilder('meta/llama-2-70b-chat'))
