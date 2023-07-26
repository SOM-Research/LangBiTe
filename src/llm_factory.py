from llm_abstract_factory import LLMFactory
from llm_huggingface_factory import HuggingFaceChatServiceBuilder, HuggingFaceServiceBuilder
from llm_openai_factory import OpenAIChatServiceBuilder, OpenAIServiceBuilder


factory = LLMFactory()

factory.register_builder('HuggingFaceGPT2', HuggingFaceServiceBuilder('https://api-inference.huggingface.co/models/gpt2'))
factory.register_builder('HuggingFaceGPT2Large', HuggingFaceServiceBuilder('https://api-inference.huggingface.co/models/gpt2-large'))
factory.register_builder('HuggingFaceGPT2XLarge', HuggingFaceServiceBuilder('https://api-inference.huggingface.co/models/gpt2-xl'))
factory.register_builder('HuggingChat', HuggingFaceChatServiceBuilder())

factory.register_builder('OpenAITextDaVinci002', OpenAIServiceBuilder('text-davinci-002'))
factory.register_builder('OpenAITextDaVinci003', OpenAIServiceBuilder('text-davinci-003'))
factory.register_builder('OpenAIGPT3.5Turbo', OpenAIChatServiceBuilder())