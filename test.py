from langbite.langbite import LangBiTe
import os
script_dir = os.path.dirname(os.path.abspath(__file__))

prompts_path = f'{script_dir}/langbite/resources/prompts_en_us.csv'
file = f'{script_dir}/documentation/examples/input_example_sexism.json'

examples = {}
examples['en_us'] = prompts_path

test = LangBiTe(prompts_path=examples, file=file)
test.generate()
test.execute()
test.report()