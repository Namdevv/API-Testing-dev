# src.graph.nodes.docs_preprocessing.section_based_chunking
from typing import Any, Dict

from langchain_core.messages import AIMessage
from pydantic import BaseModel, validate_call
from sqlmodel import Session

from src import repositories
from src.models.agent.docs_preprocessing_state_model import DocsPreProcessingStateModel
from src.settings import get_engine
from src.utils.preprocessing.section_preprocessing import (
    get_all_section_headings,
)


class DocumentMetadataProcessorNode(BaseModel):
    @validate_call
    def __call__(self, state: DocsPreProcessingStateModel) -> Dict[str, Any]:
        data = state.messages[-1].content
        doc_name = state.doc_name
        doc_url = state.doc_url
        project_id = state.project_id

        all_section_headings = get_all_section_headings(data)
        table_of_contents = "\n".join(all_section_headings)

        doc_metadata_repo = repositories.DocumentMetadataRepository(
            project_id=project_id,
            doc_name=doc_name,
            table_of_contents=table_of_contents,
            raw_doc_path=doc_url,
        )
        doc_id = doc_metadata_repo.doc_id

        with Session(get_engine()) as session:
            session.add(doc_metadata_repo)
            session.commit()

        return_data = AIMessage(
            content=data, doc_id=doc_id, all_section_headings=all_section_headings
        )

        return {
            "messages": [return_data],
        }
