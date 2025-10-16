from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import NoResultFound

from src import repositories
from src.enums import enums
from src.graph import nodes
from src.graph.workflows.docs_preprocessing import DocsPreprocessingWorkflow
from src.models import DocsPreProcessingStateModel

router = APIRouter(prefix="/document", tags=["Document"])


class DocsPreProcessingResponseModel(BaseModel):
    doc_id: str


@router.post("/docs-preprocessing")
def docs_preprocessing(
    item: DocsPreProcessingStateModel,
) -> DocsPreProcessingResponseModel:
    workflow = DocsPreprocessingWorkflow()

    result = workflow.invoke(item)
    return DocsPreProcessingResponseModel(doc_id=result["messages"][-1].content)


class GetFrInfosRequestModel(BaseModel):
    project_id: str
    lang: enums.LanguageEnum


@router.post("/get-fr-infos")
def extract_fr(
    item: GetFrInfosRequestModel, analyze: bool = False
) -> list[repositories.DocumentFRInfoRepository]:
    if not repositories.ProjectRepository.is_exist(project_id=item.project_id):
        raise HTTPException(status_code=404, detail="Project not found")

    if analyze:
        try:
            nodes.FrAnnotationNode()(item)
        except NoResultFound as e:
            raise HTTPException(status_code=404, detail=str(e))

    return repositories.DocumentFRInfoRepository.get_all_by_project_id(
        project_id=item.project_id
    )


class SelectFrInfoRequestModel(BaseModel):
    fr_info_ids: list[str]
    is_selected: bool


@router.post("/select-fr-info")
def select_fr_info(item: SelectFrInfoRequestModel) -> None:
    if repositories.DocumentFRInfoRepository.select_by_ids(
        item.fr_info_ids, is_selected=item.is_selected
    ):
        return {"message": "FR Info selection updated successfully"}

    raise HTTPException(status_code=400, detail="Failed to update FR Info selection")


@router.get("/get-docs/{project_id}")
def get_all_docs(project_id: str) -> list[repositories.DocumentMetadataRepository]:
    if not repositories.ProjectRepository.is_exist(project_id=project_id):
        raise HTTPException(status_code=404, detail="Project not found")

    documents = repositories.DocumentMetadataRepository.get_by_project_id(
        project_id=project_id
    )
    return documents


@router.post("/delete/{doc_id}")
def delete_document(doc_id: str) -> None:
    if repositories.DocumentMetadataRepository.delete_by_id(doc_id):
        return {"message": "Document deleted successfully"}

    raise HTTPException(status_code=400, detail="Document not found")
