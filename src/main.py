# --- -------------------------------------------------------------------
# --- BIAS TESTER FOR LARGE LANGUAGE MODELS
# ---
# --- A tool for testing biases in large language models.
# --- Includes a library of prompts to test bias in
# --- gender, race / skin color, nationality, politics and religion.
# --- Prompts a large language model and assess the output
# --- trying to detect sensitive words and/or unexpected
# --- unethical responses.
# --- -------------------------------------------------------------------


import os
from dotenv import load_dotenv
from prompt_io_manager import PromptIOManager
from global_evaluation import GlobalEvaluator
from prompt import Prompt
import llm_factory
from view_model import EvaluationView, ResponseView

load_dotenv()
config = {
    'openai_api_key' : os.environ["API_KEY_OPENAI"],
    'huggingface_api_key' : os.environ["API_KEY_HUGGINGFACE"]
}


# -----------------------------------------------------------------------
# query model functions
# -----------------------------------------------------------------------

def query_model(model: str, prompts: list[Prompt], responses: list, evaluations: list):
    print(f'querying {model}...')
    llmservice = llm_factory.factory.create(model, **config)
    for prompt in prompts:
        try:
            prompt.execute(llmservice)
            evaluation = prompt.evaluate()
            update_global_responses(prompt, responses)
            update_global_evaluations(prompt, evaluation, evaluations)
        except:
            update_global_responses_error(prompt, responses)
            update_global_evaluations_error(prompt, evaluations)
    print('done')


# -----------------------------------------------------------------------
# auxiliary functions
# -----------------------------------------------------------------------

def update_global_responses(prompt: Prompt, responses: list[ResponseView]):
    if len(prompt.responses) == 0:
        responses.append(ResponseView(prompt.execution_provider, prompt.execution_model, 'Template: ' + prompt.template, 'No response provided'))
    else:
        for prompt_response in prompt.responses:
            responses.append(ResponseView(prompt_response.provider, prompt_response.model, prompt_response.instance, prompt_response.response))

def update_global_evaluations(prompt: Prompt, evaluation: str, evaluations: list[EvaluationView]):
    evaluations.append(EvaluationView(prompt.execution_provider, prompt.execution_model, prompt.concern, prompt.type, prompt.assessment, prompt.template, prompt.oracle_operation, prompt.oracle_prediction, evaluation))

def update_global_responses_error(prompt: Prompt, responses: list[ResponseView]):
    for prompt_response in prompt.responses:
        responses.append(ResponseView(prompt_response.provider, prompt_response.model, prompt_response.instance, 'ERROR'))

def update_global_evaluations_error(prompt: Prompt, evaluations: list[EvaluationView]):
    evaluations.append(EvaluationView(prompt.execution_provider, prompt.execution_model, prompt.concern, prompt.type, prompt.assessment, prompt.template, prompt.oracle_operation, prompt.oracle_prediction, 'ERROR'))


# -----------------------------------------------------------------------
# main
# -----------------------------------------------------------------------

prompt_io = PromptIOManager()
prompts = prompt_io.load_prompts()

responses = []
evaluations = []

query_model('HuggingChat', prompts, responses, evaluations)
# query_model('HuggingFaceGPT2', prompts, responses, evaluations)
# query_model('HuggingFaceGPT2Large', prompts, responses, evaluations)
# query_model('HuggingFaceGPT2XLarge', prompts, responses, evaluations)
# query_model('OpenAITextDaVinci002', prompts, responses, evaluations)
# query_model('OpenAITextDaVinci003', prompts, responses, evaluations)
# query_model('OpenAIGPT3.5Turbo', prompts, responses, evaluations)

prompt_io.write_responses(responses)
prompt_io.write_evaluations(evaluations)

global_evaluator = GlobalEvaluator()
global_evaluation = global_evaluator.evaluate(evaluations)
prompt_io.write_global_evaluation(global_evaluation)