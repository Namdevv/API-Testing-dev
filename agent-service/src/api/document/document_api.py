from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src import repositories
from src.graph import nodes
from src.graph.workflows.docs_preprocessing import DocsPreprocessingWorkflow
from src.models import DocsPreProcessingStateModel
from src.enums import enums

router = APIRouter(prefix="/document", tags=["Document"])


class DocsPreProcessingResponseModel(BaseModel):
    doc_id: str


class ProjectResponseModel(BaseModel):
    project_id: str
    lang: enums.LanguageEnum


class ResponseAnnotateFRModel(BaseModel):
    fr_annotations: dict[str, list[dict[str, str]]]


@router.post("/docs-preprocessing")
def docs_preprocessing(
    item: DocsPreProcessingStateModel,
) -> DocsPreProcessingResponseModel:
    workflow = DocsPreprocessingWorkflow()

    result = workflow.invoke(item)
    return DocsPreProcessingResponseModel(doc_id=result["messages"][-1].content)


@router.post("/annotate-fr")
def annotate_fr(
    item: ProjectResponseModel,
) -> ResponseAnnotateFRModel:
    node = nodes.FrAnnotationNode()

    result = node(item)
    return ResponseAnnotateFRModel(fr_annotations=result["messages"][-1].content[-1])


@router.get("/all/{project_id}")
def get_all_projects(project_id: str) -> list[repositories.DocumentMetadataRepository]:
    documents = repositories.DocumentMetadataRepository.get_by_project_id(
        project_id=project_id
    )
    return documents


@router.post("/delete/{doc_id}")
def delete_document(doc_id: str) -> None:
    if repositories.DocumentMetadataRepository.delete_by_id(doc_id):
        return {"message": "Document deleted successfully"}

    raise HTTPException(status_code=400, detail="Document not found")
