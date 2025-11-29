# src.graph.nodes.testcase_generator.document_standardizer
import logging
from typing import Optional

from pydantic import validate_call

from src.base.service.base_agent_service import BaseAgentService
from src.enums.enums import LanguageEnum
from src.models import TestcasesGenStateModel


class DocumentStandardizer(BaseAgentService):
    llm_model: str = "gemini-2.5-flash"
    llm_temperature: float = 0

    llm_top_p: Optional[float] = 0.1

    llm_thinking_budget: Optional[int] = -1

    path_to_prompt: dict[LanguageEnum, str] = {
        LanguageEnum.VI: "src/graph/nodes/testcase_generator/prompts/document_standardizer_vi.md",
        LanguageEnum.EN: "src/graph/nodes/testcase_generator/prompts/document_standardizer_en.md",
    }

    @validate_call
    def __call__(self, state: TestcasesGenStateModel) -> TestcasesGenStateModel:
        collected_documents = state.extra_parameters.get("collected_documents", None)

        all_fr_infos = state.extra_parameters["all_fr_infos"]
        current_fr_index = state.extra_parameters.get("current_fr_index", -1)
        current_fr_id = all_fr_infos[current_fr_index].fr_info_id

        if not collected_documents:
            raise ValueError("No collected documents found in state.extra_parameters")
        lang = state.lang
        self.set_system_lang(lang)

        standardized_documents = self.run(
            human=collected_documents[current_fr_id]
        ).content

        state.extra_parameters["standardized_documents"][
            current_fr_id
        ] = standardized_documents
        logging.info("Document standardization completed!")
        return state


if __name__ == "__main__":
    from .document_collector import DocumentCollector
    from .document_preparator import DocumentPreparator

    document_preparator = DocumentPreparator()
    response = document_preparator(
        TestcasesGenStateModel(
            project_id="ae4750b9-fc21-4510-a2f4-bb7d3c47b830",
            lang=LanguageEnum.EN,
        )
    )
    document_collector = DocumentCollector()
    response = document_collector(response)

    document_standardizer = DocumentStandardizer()
    response = document_standardizer(response)

    print(response.extra_parameters.get("standardized_documents"))
