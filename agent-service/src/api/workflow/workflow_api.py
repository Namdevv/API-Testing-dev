from fastapi import APIRouter
from pydantic import BaseModel

from src.graph.workflows.docs_preprocessing import DocsPreprocessingWorkflow
from src.models.agent.docs_preprocessing_state_model import DocsPreProcessingStateModel

router = APIRouter(prefix="/workflow", tags=["Workflow"])


class DocsPreProcessingResponseModel(BaseModel):
    doc_id: str


@router.post("/docs-preprocessing")
def docs_preprocessing(
    item: DocsPreProcessingStateModel,
) -> DocsPreProcessingResponseModel:
    workflow = DocsPreprocessingWorkflow()

    result = workflow.invoke(item)
    return DocsPreProcessingResponseModel(doc_id=result["messages"][-1].content)
