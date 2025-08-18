from typing import Annotated, List

from langgraph.graph.message import add_messages
from pydantic import (
    BaseModel,
    Field,
)


class DocsPreProcessingStateModel(BaseModel):
    """
    Represents the state of an AI agent, including its name, description, and current status.
    """

    lang: str = Field(
        default_factory=str,
        description="Language of the document",
    )

    data: Annotated[List, add_messages] = []  # Messages in string format
