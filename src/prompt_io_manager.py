import pandas
import numpy as np
from prompt import Prompt
import oracle_factory


class PromptIOManager:

    RESPONSES_FILENAME = 'generated_responses'
    EVALUATIONS_FILENAME = 'generated_evaluations'
    GLOBAL_EVALUATION_FILENAME = 'global_evaluation'

    def load_prompts(self):
        # reads a csv file containing the prompts, with the following columns:
        # - 0: prompt id
        # - 1: concern
        # - 2: prompt type
        # - 3: assessment type
        # - 4: task prefix
        # - 5: prompt template
        # - 6: output formatting instructions
        # - 7: oracle type
        # - 8: oracle prediction / evaluation expression
        prompts_df = pandas.read_csv('resources/prompts.csv', sep='\t')
        all_prompts = []
        for value in prompts_df.values.tolist():
            prompt = Prompt(id=value[0],
                            concern=value[1],
                            type=value[2],
                            assessment=value[3],
                            task_prefix=value[4] if value[4] is not np.nan else None,
                            template=value[5],
                            output_formatting=value[6],
                            oracle=oracle_factory.factory.create(key=value[7],prediction=value[8],prompt_id=value[0]))
            all_prompts.append(prompt)
        return all_prompts