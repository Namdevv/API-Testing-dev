# src.graph.nodes.testcase_generator.testcase_generator
import logging
from typing import Any, Dict

from langchain_core.output_parsers import JsonOutputParser
from pydantic import validate_call

from src.base.service.base_agent_service import BaseAgentService
from src.enums.enums import LanguageEnum
from src.models import TestcasesGenStateModel


class TestCaseGenerator(BaseAgentService):
    llm_model: str = "vllm-QC-AI"
    llm_temperature: float = 0.0

    path_to_prompt: dict[LanguageEnum, str] = {
        LanguageEnum.VI: "src/graph/nodes/testcase_generator/prompts/testcase_generator_vi.md",
        LanguageEnum.EN: "src/graph/nodes/testcase_generator/prompts/testcase_generator_en.md",
    }

    def extract_clean_json_from_text(self, raw_text):
        """
        Clean a single text block & extract JSON test case.
        """
        json_parser = JsonOutputParser()
        data = json_parser.parse(raw_text)

        if isinstance(data, list):
            data = data[-1]
        elif isinstance(data, dict):
            pass

        return {
            "request_body": data.get("request_body", {}),
            "testcases": data.get("testcases", {}),
        }

    @validate_call
    def __call__(self, state: TestcasesGenStateModel) -> Dict[str, Any]:
        lang = state.lang
        current_fr = state.extra_parameters["current_fr"]
        standardized_documents = state.extra_parameters["standardized_documents"][
            current_fr
        ]
        self.set_system_lang(lang)

        response = self.run(human=standardized_documents).content

        response = self.extract_clean_json_from_text(response)

        state.test_case_infos[current_fr] = response
        logging.info(f"Generated test cases for FR group: {current_fr}")
        return state


if __name__ == "__main__":
    from .document_collector import DocumentCollector
    from .document_preparator import DocumentPreparator
    from .document_standardizer import DocumentStandardizer

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

    testcase_generator = TestCaseGenerator()
    response = testcase_generator(response)

    print(response.testcases)
