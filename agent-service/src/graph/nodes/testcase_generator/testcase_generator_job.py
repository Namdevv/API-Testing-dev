# src.graph.nodes.testcase_generator.testcase_generator
import logging
from typing import Any, Dict

from pydantic import BaseModel, validate_call

from src.models import TestcasesGenStateModel


class TestcaseGeneratorJob(BaseModel):
    @validate_call
    def __call__(self, state: TestcasesGenStateModel) -> Dict[str, Any]:
        all_fr_groups = state.extra_parameters["all_fr_groups"]

        # Initialize
        if not state.extra_parameters.get("current_fr", None):
            state.extra_parameters["collected_documents"] = {}
            state.extra_parameters["standardized_documents"] = {}

        progress = ""
        if all_fr_groups:
            current_fr = all_fr_groups.pop(0)
            logging.info(f"Current FR group to process: {current_fr}")
            progress = "in_progress"
        else:
            logging.info("All FR groups have been processed. Job completed.")
            progress = "completed"

        state.extra_parameters["all_fr_groups"] = all_fr_groups
        state.extra_parameters["progress"] = progress
        state.extra_parameters["current_fr"] = (
            current_fr if progress == "in_progress" else None
        )

        return state


def orchestrate_job(state: TestcasesGenStateModel) -> str:
    return state.extra_parameters.get("progress", "completed")


if __name__ == "__main__":
    pass
