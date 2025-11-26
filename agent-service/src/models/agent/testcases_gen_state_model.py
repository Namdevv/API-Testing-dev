from typing import Annotated, Any, List, Optional

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, ConfigDict, Field

from src.enums.enums import LanguageEnum


class TestcasesGenStateModel(BaseModel):
    """
    Represents the state of an AI agent, including its name, description, and current status.
    """

    project_id: str = Field(
        description="Project ID, must be unique.",
    )

    lang: LanguageEnum = Field(
        default=LanguageEnum.EN,
        description="Language of the document",
    )

    all_fr_groups: list[str] = Field(
        default_factory=list,
        description="List of functional requirements to generate test cases for",
    )

    testcases: list[dict[str, Any]] = Field(
        default_factory=list,
        description="List of generated test cases",
    )

    messages: Annotated[List[BaseMessage], add_messages] = Field(
        default_factory=list,
        description="Messages exchanged during the conversation",
    )

    last_extra_parameter: Optional[str] = Field(
        default=None,
        description="The key of the last extra parameter added",
    )

    extra_parameters: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional parameters for processing",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "project_id": "00000000-0000-0000-0000-000000000000",
                "lang": "en",
            }
        }
    )
