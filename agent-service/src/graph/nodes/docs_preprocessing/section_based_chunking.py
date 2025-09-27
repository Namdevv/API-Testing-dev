# src.graph.nodes.docs_preprocessing.section_based_chunking
from typing import Any, Dict

from langchain_core.messages import AIMessage
from pydantic import validate_call

from src import cache
from src.base.service.base_agent_service import BaseAgentService
from src.enums.enums import LanguageEnum
from src.models.agent.docs_preprocessing_state_model import DocsPreProcessingStateModel
from src.models.document.document_model import DocumentModel
from src.repositories.document.document_repository import DocumentRepository
from src.utils.common import split_by_size
from src.utils.preprocessing import section_preprocessing


class SectionBasedChunkingNode(DocumentRepository):
    llm_model: str = "gemma-3-27b-it"
    llm_temperature: float = 0.0
    llm_top_p: float = 0.1
    llm_top_k: int = 3

    batch_size: int = 10
    max_workers: int = 2

    path_to_prompt: dict[LanguageEnum, str] = {
        LanguageEnum.VI: "src/graph/nodes/docs_preprocessing/prompts/section_based_chunking_vi.txt",
        LanguageEnum.EN: "src/graph/nodes/docs_preprocessing/prompts/section_based_chunking_en.txt",
    }

    @validate_call
    def __call__(self, state: DocsPreProcessingStateModel) -> Dict[str, Any]:
        data = state.messages[-1].content
        doc_id = state.messages[-1].doc_id
        all_section_headings = state.messages[-1].all_section_headings

        section_to_content = section_preprocessing.extract_section_contents(
            data, all_section_headings
        )
        parent_child_blocks = section_preprocessing.create_parent_child_blocks(
            all_section_headings
        )
        print(f"Parent-child blocks: {parent_child_blocks}")
        hierarchical_section_blocks = (
            section_preprocessing.create_hierarchical_section_blocks(
                section_to_content, parent_child_blocks
            )
        )

        docs = [
            DocumentModel(
                doc_id=doc_id,
                text=hierarchical_section_block,
            )
            for hierarchical_section_block in hierarchical_section_blocks
        ]

        batches = split_by_size(docs, self.batch_size)
        for batch in batches:
            self.create_records(data=batch, overwrite=True)

        # result = self.__chunk_and_annotate(data)

        return_data = AIMessage(content=doc_id)

        return {
            "messages": [return_data],
        }
