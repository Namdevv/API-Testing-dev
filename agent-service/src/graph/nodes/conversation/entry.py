# src.graph.nodes.docs_preprocessing.data_cleaning
from typing import Any, Dict

from langchain_core.messages import HumanMessage

from src.registry.nodes import register_node


@register_node("conversation.entry")
class Entry:
    def __call__(self, state) -> Dict[str, Any]:

        return {
            "messages": [HumanMessage(content=state.user_input)],
        }
