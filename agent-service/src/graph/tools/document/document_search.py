# src.graph.tools.document.document_search
from typing import Optional

from langchain.tools import tool
from sqlmodel import Session, select

from src.base.service.base_embedding_service import BaseEmbeddingService
from src.cache import cache_func_wrapper
from src.repositories.document.document_content_repository import (
    DocumentContentRepository,
)
from src.repositories.document.document_metadata_repository import (
    DocumentMetadataRepository,
)
from src.settings import get_db_engine


# @tool
@cache_func_wrapper
def search_documents(
    query: str,
    project_id: Optional[str] = "",
    doc_id: Optional[str] = "",
    top_k: int = 10,
):
    """
    Search documents in the specified project using vector similarity.

    Args:
        query (str): The search query.
        project_id (str): The ID of the project to search within.
        doc_id (str): The ID of the document to search within.
        top_k (int): The number of top similar documents to return.
    Returns:
        list[DocumentContentRepository]: A list of the top_k most similar document contents.
    """
    embedding = BaseEmbeddingService()
    embedded_vector = embedding.embed_query(query)

    with Session(get_db_engine()) as session:
        result = session.exec(
            select(DocumentContentRepository)
            .join(DocumentMetadataRepository)
            .where(
                (DocumentMetadataRepository.project_id == project_id)
                | (DocumentMetadataRepository.doc_id == doc_id)
            )
            .order_by(DocumentContentRepository.vector.cosine_distance(embedded_vector))
            .limit(top_k)
        )
        return result.all()


if __name__ == "__main__":

    result = search_documents(
        "create project, api details", "a5f3da9d-c7f7-4f7e-b92c-478304dcf9f7", top_k=10
    )

    for r in result:
        print(r.text)
