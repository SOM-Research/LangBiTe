from dotenv import load_dotenv
import os
import time
import pandas
from langbite.controllers.global_evaluation import GlobalEvaluation
from langbite.model.view_model import EvaluationView, ResponseView


class ReportingIOManager:
    RESPONSES_FILENAME = 'responses'
    EVALUATIONS_FILENAME = 'evaluations'
    GLOBAL_EVALUATION_FILENAME = 'global_evaluation'
    REPORTS_PATH = 'reports'
    
    def set_path(self, path):
        self.REPORTS_PATH = path
        
    def write_responses(self, responses: list[ResponseView]):
        return self.write_list(responses, self.RESPONSES_FILENAME)
    
    def write_evaluations(self, evaluations: list[EvaluationView]):
        return self.write_list(evaluations, self.EVALUATIONS_FILENAME)
    
    def write_global_evaluation(self, global_evaluation: list[GlobalEvaluation]):
        return self.write_list(global_evaluation, self.GLOBAL_EVALUATION_FILENAME)
    
    def write_list(self, elements: list[any], filename: any):
        if len(elements) == 0: return
        elements_df = pandas.DataFrame.from_records([e.to_dict() for e in elements])
        print(elements_df)
        write_report_to_file = os.environ.get("WRITE_REPORT_TO_FILE", "false").lower() == "true"
        if write_report_to_file:
            self.write_output_file(elements_df, filename)
        return elements_df
    
    def write_output_file(self, dataframe, filename):
        timestamp = time.strftime("%Y%m%d%H%M%S")
        filename = f'{timestamp}_{filename}.csv'
 
        #dataframe.to_csv(full_path, encoding='utf-8', index=False)
        print(os.path.join(self.REPORTS_PATH,filename))
        dataframe.to_csv(os.path.join(self.REPORTS_PATH,filename))