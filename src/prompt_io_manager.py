import random
import time
import pandas
import numpy as np
from prompt import Prompt
import oracle_factory
from global_evaluation import GlobalEvaluation
from view_model import EvaluationView, ResponseView


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
        result = []
        for value in prompts_df.values.tolist():
            prompt = Prompt(id=value[0],
                            concern=value[1],
                            type=value[2],
                            assessment=value[3],
                            task_prefix=value[4] if value[4] is not np.nan else None,
                            template=value[5],
                            output_formatting=value[6],
                            oracle=oracle_factory.factory.create(key=value[7],prediction=value[8],prompt_id=value[0]))
            result.append(prompt)
        return random.sample(result, 10)
    
    def write_responses(self, responses: list[ResponseView]):
        if len(responses) == 0: return
        # format output
        responses_df = pandas.DataFrame.from_records([r.to_dict() for r in responses])
        #responses_df.columns = ['Provider', 'Model', 'Template', 'Response']
        #responses_df = responses_df.replace(r'\r+|\n+|\t+','', regex=True)
        #responses_df['Response'] = (responses_df['Response'].str.split()).str.join(' ')
        # print output
        print(responses_df)
        # save output to csv
        self.write_output_file(responses_df, self.RESPONSES_FILENAME)
    
    def write_evaluations(self, evaluations: list[EvaluationView]):
        if len(evaluations) == 0: return
        # format output
        evaluations_df = pandas.DataFrame.from_records([e.to_dict() for e in evaluations])
        #evaluations_df.columns = ['Provider', 'Model', 'Concern', 'Type', 'Assessment', 'Template', 'Oracle Operation', 'Oracle Prediction', 'Evaluation']
        # print output
        print(evaluations_df)
        # save output to csv
        self.write_output_file(evaluations_df, self.EVALUATIONS_FILENAME)
    
    def write_global_evaluation(self, global_evaluation: list[GlobalEvaluation]):
        if len(global_evaluation) == 0: return
        # format output
        evaluations_df = pandas.DataFrame.from_records([ge.to_dict() for ge in global_evaluation])
        #evaluations_df.columns = ['Provider', 'Model', 'Concern', 'Type', 'Assessment', 'Nr of Passed', 'Nr of Failed', 'Pct of Passed', 'Pct of Failed', 'Total']
        # print output
        print(evaluations_df)
        # save output to csv
        self.write_output_file(evaluations_df, self.GLOBAL_EVALUATION_FILENAME)
    
    def write_output_file(self, dataframe, filename):
        timestamp = time.strftime("%Y%m%d%H%M%S")
        full_path = f'outputs\_{filename}_{timestamp}.csv'
        dataframe.to_csv(full_path, encoding='utf-8', index=False)