from dotenv import load_dotenv
import os

def load_api_keys():
    load_dotenv()
    config = {
        'openai_api_key' : os.environ["API_KEY_OPENAI"],
        'huggingface_api_key' : os.environ["API_KEY_HUGGINGFACE"],
        'replicate_api_key': os.environ["API_KEY_REPLICATE"],
        'ollama_url': os.environ["OLLAMA_URL"]
    }
    return config