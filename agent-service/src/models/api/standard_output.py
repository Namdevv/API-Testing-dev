from pydantic import BaseModel


class ResultModel(BaseModel):
    code: list[str]
    description: str


class StandardOutputModel(BaseModel):
    result: ResultModel
    data: dict
