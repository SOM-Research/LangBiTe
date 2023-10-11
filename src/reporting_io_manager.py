import os
import time
import pandas
from global_evaluation import GlobalEvaluation
from view_model import EvaluationView, ResponseView


class ReportingIOManager:

    RESPONSES_FILENAME = 'responses'
    EVALUATIONS_FILENAME = 'evaluations'
    GLOBAL_EVALUATION_FILENAME = 'global_evaluation'
    
    def write_responses(self, responses: list[ResponseView]):
        self.write_list(responses, self.RESPONSES_FILENAME)
    
    def write_evaluations(self, evaluations: list[EvaluationView]):
        self.write_list(evaluations, self.EVALUATIONS_FILENAME)
    
    def write_global_evaluation(self, global_evaluation: list[GlobalEvaluation]):
        self.write_list(global_evaluation, self.GLOBAL_EVALUATION_FILENAME)
    
    def write_list(self, elements: list[any], filename: any):
        if len(elements) == 0: return
        elements_df = pandas.DataFrame.from_records([e.to_dict() for e in elements])
        print(elements_df)
        self.write_output_file(elements_df, filename)
    
    def write_output_file(self, dataframe, filename):
        timestamp = time.strftime("%Y%m%d%H%M%S")
        filename = f'{timestamp}_{filename}.csv'
        path = f'reports'
        #dataframe.to_csv(full_path, encoding='utf-8', index=False)
        dataframe.to_csv(os.path.join(path,filename))