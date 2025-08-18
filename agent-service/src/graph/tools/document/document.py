from typing import Type

from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from src.registry.tools import register_tool
from src.repositories.document.document_repository import DocumentRepository

register_tool("document.document_tool")


class _DocumentInput(BaseModel):
    query: str = Field(description="The query text to search for")
    doc_name: str = Field(description="The name of the document")
    annotations: str = Field(description="Annotations to filter the documents")
    document_amount: int = Field(
        default=1, description="The number of documents to return"
    )
    document_offset: int = Field(default=0, description="The offset for pagination")


class DocumentTool(BaseTool):
    name: str = "document_tool"
    description: str = """
    Tool for search document by text, and other metadata

    Args:
        query: The query text to search for
        doc_name: The name of the document
        annotations: Annotations to filter the documents
        document_amount: The number of documents to return
        document_offset: The offset for pagination

    Returns:
        A list of documents matching the search criteria.
    """
    args_schema: Type[BaseModel] = _DocumentInput

    def __init__(self):
        self.__repository = DocumentRepository()

    def _run(
        self,
        query: str,
        document_amount: int = 1,
        document_offset: int = 0,
        doc_name: str = None,
        annotations: str = None,
    ):
        return self.__repository.search_documents(
            query=query,
            doc_name=doc_name,
            annotations=annotations,
            document_amount=document_amount,
            document_offset=document_offset,
        )
