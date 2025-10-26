from typing import Any, Dict

from langchain_core.messages import AIMessage
from pydantic import validate_call

from enums.enums import LanguageEnum
from src.base.service.base_agent_service import BaseAgentService
from src.common.preprocessing import section_preprocessing, text_preprocessing
from src.models import DocsPreProcessingStateModel


class DocCollector(BaseAgentService):
    llm_model: str = "gemini-2.0-flash-lite"
    llm_temperature: float = 0.0
    llm_top_p: float = 0.1
    llm_top_k: int = 3

    path_to_prompt: dict[LanguageEnum, str] = {
        LanguageEnum.VI: "src/graph/nodes/testcase_generator/prompts/doc_collector_vi.txt",
        LanguageEnum.EN: "src/graph/nodes/testcase_generator/prompts/doc_collector_en.txt",
    }

    @validate_call
    def __call__(self, state: DocsPreProcessingStateModel) -> Dict[str, Any]:
        data = state.messages[-1].content
        self.set_system_lang()

        output = self.run({"input": data, "chat_history": state.messages[-5:]})

        return {
            "messages": [output],
        }
