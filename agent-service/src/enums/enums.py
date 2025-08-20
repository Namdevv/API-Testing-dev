from enum import Enum


class ModelTypeEnum(str, Enum):
    llm = "llm"
    embedding = "embedding"


class LanguageEnum(str, Enum):
    vi = "vi"
    en = "en"
