from langbite.llm_abstract_factory import LLMFactory
from langbite.llm_huggingface_factory import HuggingFaceChatServiceBuilder, HuggingFaceCompletionServiceBuilder, HuggingFaceQuestionAnsweringServiceBuilder
from langbite.llm_openai_factory import OpenAIChatServiceBuilder, OpenAIServiceBuilder


factory = LLMFactory()

factory.register_builder('HuggingFaceGPT2', HuggingFaceCompletionServiceBuilder('https://api-inference.huggingface.co/models/gpt2'))
factory.register_builder('HuggingFaceGPT2Large', HuggingFaceCompletionServiceBuilder('https://api-inference.huggingface.co/models/gpt2-large'))
factory.register_builder('HuggingFaceGPT2XLarge', HuggingFaceCompletionServiceBuilder('https://api-inference.huggingface.co/models/gpt2-xl'))
factory.register_builder('HuggingFaceBlenderBot', HuggingFaceCompletionServiceBuilder('https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill'))
factory.register_builder('HuggingFacePersonaGPT', HuggingFaceCompletionServiceBuilder('https://api-inference.huggingface.co/models/af1tang/personaGPT'))
factory.register_builder('HuggingFaceDialoGPT', HuggingFaceCompletionServiceBuilder('https://api-inference.huggingface.co/models/microsoft/DialoGPT-large'))
factory.register_builder('HuggingFaceSmallRickSanchez', HuggingFaceCompletionServiceBuilder('https://api-inference.huggingface.co/models/AJ/DialoGPT-small-ricksanchez'))
# this next two are for question answering, may require different invoke method
factory.register_builder('HuggingFaceRobertaBaseSquad2', HuggingFaceQuestionAnsweringServiceBuilder('https://api-inference.huggingface.co/models/deepset/roberta-base-squad2'))
factory.register_builder('HuggingFaceDistilbertBaseUncased', HuggingFaceQuestionAnsweringServiceBuilder('https://api-inference.huggingface.co/models/distilbert-base-uncased-distilled-squad'))

factory.register_builder('HuggingChat', HuggingFaceChatServiceBuilder())

factory.register_builder('OpenAITextCurie001', OpenAIServiceBuilder('text-curie-001'))
factory.register_builder('OpenAITextBabbage001', OpenAIServiceBuilder('text-babbage-001'))
factory.register_builder('OpenAITextAda001', OpenAIServiceBuilder('text-ada-001'))
factory.register_builder('OpenAITextDaVinci003', OpenAIServiceBuilder('text-davinci-003'))

factory.register_builder('OpenAIGPT35Turbo0301', OpenAIChatServiceBuilder('gpt-3.5-turbo-0301')) # snapshot March 1st, 2023
factory.register_builder('OpenAIGPT35Turbo0613', OpenAIChatServiceBuilder('gpt-3.5-turbo-0613')) # snapshot June 13th, 2023

factory.register_builder('OpenAIGPT40314', OpenAIChatServiceBuilder('gpt-4-0314')) # snapshot March 14th, 2023
factory.register_builder('OpenAIGPT40613', OpenAIChatServiceBuilder('gpt-4-0613')) # snapshot June 13th, 2023

factory.register_builder('OpenAIGPT35Turbo', OpenAIChatServiceBuilder('gpt-3.5-turbo'))
factory.register_builder('OpenAIGPT35Turbo16k', OpenAIChatServiceBuilder('gpt-3.5-turbo-16k'))
factory.register_builder('OpenAIGPT4', OpenAIChatServiceBuilder('gpt-4'))