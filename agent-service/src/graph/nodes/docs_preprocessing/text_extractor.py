# src.graph.nodes.docs_preprocessing.text_extractor
import logging
from typing import Any, Dict

from docling.document_converter import DocumentConverter, InputFormat
from dotenv import load_dotenv

from src.base.service.base_agent_service import BaseAgentService

# prompt_vn = None
# with open(
#     "src/graph/nodes/docs_preprocessing/prompts/metadata_removal_vn.txt", "r"
# ) as f:
#     prompt_vn = f.read()

# prompt_en = None
# with open(
#     "src/graph/nodes/docs_preprocessing/prompts/metadata_removal_en.txt", "r"
# ) as f:
#     prompt_en = f.read()


# class MetaDataRemoval(BaseAgentService):
#     llm_model: str = "gemini-2.0-flash-lite"
#     llm_temperature: float = 0.0
#     llm_top_p: float = 0.1
#     llm_top_k: int = 3

#     def __call__(self, state) -> Dict[str, Any]:
#         data = state.data
#         lang = state.lang

#         if lang == "vi":
#             self.system_prompt = prompt_vn
#         else:
#             self.system_prompt = prompt_en

#         invoke_input = {
#             "input": data,
#             "chat_history": [],
#         }

#         response = self.run(invoke_input)

#         logging.info("MetaDataRemoval node called")

#         return {
#             "messages": [response],
#         }


if __name__ == "__main__":
    source = "/mnt/Data/API-Testing/agent-service/static/data/hehe.pdf"  # document per local path or URL
    converter = DocumentConverter()

    result = converter.convert(source, max_num_pages=1)
    print(
        result.document.export_to_markdown()
    )  # output: "## Docling Technical Report[...]"
