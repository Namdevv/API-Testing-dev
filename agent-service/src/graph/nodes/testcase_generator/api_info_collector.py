# src.graph.nodes.testcase_generator.testcase_generator
import logging
from typing import Any, Dict, Optional

from langchain_core.output_parsers import JsonOutputParser
from pydantic import validate_call

from src.base.service.base_agent_service import BaseAgentService
from src.enums.enums import LanguageEnum
from src.models import TestcasesGenStateModel


class APIInfoCollector(BaseAgentService):
    llm_model: str = "gemini-2.5-flash-lite"
    llm_temperature: float = 0.0

    llm_thinking_budget: Optional[int] = -1

    path_to_prompt: dict[LanguageEnum, str] = {
        LanguageEnum.VI: "src/graph/nodes/testcase_generator/prompts/api_info_collector_vi.md",
        LanguageEnum.EN: "src/graph/nodes/testcase_generator/prompts/api_info_collector_en.md",
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

        json_parser = JsonOutputParser()
        response = json_parser.parse(response)

        state.test_case_infos[current_fr]["api_info"] = response

        logging.info("API info collection completed!")
        return state


if __name__ == "__main__":
    pass
