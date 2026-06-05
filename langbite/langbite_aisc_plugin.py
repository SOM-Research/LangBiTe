import sys
import time
from typing import Any

import pandas as pd
from pandas import DataFrame

from aisc_plugin_interface import (
    BaseEvaluationPlugin,
    InputType,
    TaskProgress,
    evaluation_input,
    metric,
)
from aisc_plugin_interface.models.measure import Measure

from langbite.aisc_plugin.custom_dataset_input_provider import CustomDatasetInputProvider
from langbite.aisc_plugin.models import ConfigFormSchema, LanguageEnum
from langbite.aisc_plugin.ui_schema import ui_schema

DATASET_INPUT = "dataset"


def _error_result(message: str) -> dict:
    print(f"[LangBiTe] ERROR: {message}", file=sys.stderr)
    return {"global_evaluation": [], "status": "error", "error": message}


@evaluation_input(
    name=DATASET_INPUT,
    label="Prompt Template (TSV)",
    input_provider_class=CustomDatasetInputProvider,
    input_type=InputType.DATASET,
    required=True,
)
class LangBiteEvaluationPlugin(BaseEvaluationPlugin[ConfigFormSchema]):
    plugin_name = "LangBiTe"
    ui_icon = "science"
    form_ui_schema = ui_schema

    # LangBiTe-native: map the form schema onto the internal config LangBiTe expects.
    def form_schema_to_internal(self, config_form_data: ConfigFormSchema) -> dict:
        config_data = config_form_data.model_dump()
        config_data["aiModels"] = [config_data["aiModels"]]
        for requirement in config_data["requirements"]:
            communities = {}
            languages = []
            for community in requirement["communities"]:
                communities[community["language"]] = community["entries"]
                languages.append(LanguageEnum(community["language"]))
            requirement["languages"] = languages
            requirement["communities"] = communities
        config_data["timestamp"] = int(time.time())
        return config_data

    def evaluate(self, config_data) -> Any:
        try:
            return self._run_evaluation(config_data)
        except Exception as exc:
            import traceback
            print(f"[LangBiTe] Unhandled exception:\n{traceback.format_exc()}", file=sys.stderr)
            return _error_result(str(exc))

    def _run_evaluation(self, config_data) -> dict:
        from langbite.langbite import LangBiTeForAPI

        config: ConfigFormSchema = self.validate_config_form_data(config_data)
        langbite_config = self.form_schema_to_internal(config)
        input_language = langbite_config["language"]

        self.report_progress(TaskProgress(progress=0.05, extra={"stage": "setup"}))

        prompts = self.get_input_data(DATASET_INPUT)
        if not prompts:
            return _error_result("No prompt template provided. Upload a TSV prompt template.")

        self.report_progress(TaskProgress(progress=0.40, extra={"stage": "executing"}))

        langbite = LangBiTeForAPI({
            "prompts": prompts,
            "config": langbite_config,
            "input_language": input_language,
        })
        langbite.generate()
        langbite.execute()
        report = langbite.report()

        # Normalise LangBiTe's report (global_eval DataFrame) into JSON records so
        # the metrics below can consume a plain dict.
        global_eval = report.get("global_eval")
        if isinstance(global_eval, DataFrame):
            global_records = global_eval.to_dict(orient="records")
            self.upload_artifact(
                "global_evaluation.csv",
                global_eval.to_csv(index=False, sep=";").encode(),
            )
        else:
            global_records = list(global_eval) if global_eval else []

        self.report_progress(TaskProgress(progress=0.95, extra={"stage": "done"}))
        return {"global_evaluation": global_records, "status": "success"}

    # ── Metrics (ported from the MLA-BiTe plugin, rebranded LangBiTe) ──────────
    @metric("LangBiTe Run Success")
    def export_run_success(self, evaluation_output: dict) -> list[Measure]:
        score = 1.0 if evaluation_output.get("status") == "success" else 0.0
        description = evaluation_output.get("error") or "LangBiTe execution finished"
        return [Measure(name="LangBiTe Run Success", score=score, description=description)]

    @metric("Bias Evaluation Results")
    def export_bias_results(self, evaluation_output: dict) -> list[Measure]:
        measures = []
        for row in evaluation_output.get("global_evaluation", []):
            name = (
                f"{row.get('Concern', '')} | {row.get('Model', '')} | "
                f"{row.get('Language', '')} | {row.get('Input Type', '')} | "
                f"{row.get('Reflection Type', '')}"
            )
            total = row.get("Total", 0)
            description = (
                f"Tolerance Evaluation: {row.get('Tolerance Evaluation', 'Unknown')} | "
                f"Tolerance: {row.get('Tolerance', '')} | "
                f"Passed: {row.get('Passed Nr', 0)}/{total} | "
                f"Failed: {row.get('Failed Nr', 0)}/{total}"
            )
            measures.append(
                Measure(name=name, score=float(row.get("Passed Pct", 0.0)), description=description)
            )
        return measures

    @metric("Overall Pass Rate")
    def export_overall_pass_rate(self, evaluation_output: dict) -> list[Measure]:
        rows = evaluation_output.get("global_evaluation", [])
        if not rows:
            error = evaluation_output.get("error", "")
            return [Measure(name="Overall Pass Rate", score=0.0, description=error or "No evaluations produced")]
        avg = sum(float(r.get("Passed Pct", 0.0)) for r in rows) / len(rows)
        return [Measure(name="Overall Pass Rate", score=avg)]

    @metric("All Tolerances Passed")
    def export_all_tolerances_passed(self, evaluation_output: dict) -> list[Measure]:
        rows = evaluation_output.get("global_evaluation", [])
        n_passed = sum(1 for r in rows if r.get("Tolerance Evaluation") == "Passed")
        all_passed = bool(rows) and n_passed == len(rows)
        return [
            Measure(
                name="All Tolerances Passed",
                score=1.0 if all_passed else 0.0,
                description=f"{n_passed}/{len(rows)} tolerance checks passed",
            )
        ]
