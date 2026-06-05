from enum import Enum

from pydantic import BaseModel, Field, model_validator


class AIModelProvider(str, Enum):
    GPT4ALL = "GPT4ALL"


class LanguageEnum(str, Enum):
    en_us = "en_us"
    es_es = "es_es"
    ca_es = "ca_es"
    fr_fr = "fr_fr"


class RequirementInputs(str, Enum):
    constrained = "constrained"
    verbose = "verbose"


class RequirementReflections(str, Enum):
    observational = "observational"
    utopian = "utopian"


class Communities(BaseModel):
    language: LanguageEnum = Field(..., title="Select Language")
    entries: list[str] = Field(
        default_factory=list,
        title="Community Strings"
    )


class RequirementsSchema(BaseModel):
    @model_validator(mode='after')
    def check_lengths(self):
        lengths = [len(community.entries) for community in self.communities]
        if lengths and len(set(lengths)) > 1:
            raise ValueError("Inconsistent list lengths found in communities.")
        return self

    name: str = Field(..., title="Requirement Name")
    rationale: str = Field(..., title="Rationale")
    languages: set[LanguageEnum] = Field(
        default=[],
        title="Supported Languages"
    )
    tolerance: float = Field(0.9, ge=0, le=1)
    delta: float = Field(0.02)
    concern: str = Field(...)
    markup: str = Field(...)
    communities: list[Communities] = Field(
        default_factory=list,
        title="Communities"
    )
    inputs: set[RequirementInputs] = Field(
        default=[input.value for input in RequirementInputs],
        title="Inputs"
    )
    reflections: set[RequirementReflections] = Field(default=[reflection.value for reflection in RequirementReflections], title="Reflections")


class ConfigFormSchema(BaseModel):
    nTemplates: int = Field(default=60, title="Number of templates")
    nRetries: int = Field(default=1, title="Number of templates")
    temperature: float = Field(default=1.0, ge=0, le=2, title="Temperature")
    tokens: int = Field(default=60, title="Number of tokens")
    useLLMEval: bool = Field(default=True, title="Use LLMEval")
    aiModels: AIModelProvider = Field(
        default=AIModelProvider.GPT4ALL,
        title="Select AI Model",
        description="Choose the primary model for this evaluation"
    )
    requirements: list[RequirementsSchema] = Field(default=list, title="Requirements")
    language: LanguageEnum = Field(
        default=LanguageEnum.en_us,
        title="Language to run"
    )
    