from fastapi import APIRouter

from src.graph.workflows.docs_preprocessing import DocsPreprocessingWorkflow
from src.models.agent.docs_preprocessing_state_model import DocsPreProcessingStateModel

router = APIRouter(prefix="/workflow", tags=["Workflow"])


@router.post("/docs-preprocessing")
def docs_preprocessing(
    item: DocsPreProcessingStateModel,
) -> DocsPreProcessingStateModel:
    workflow = DocsPreprocessingWorkflow()

    return workflow.invoke(item)
