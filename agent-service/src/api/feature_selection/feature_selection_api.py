from contextlib import asynccontextmanager
from typing import Optional

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

from src.repositories.document.document_repository import DocumentRepository

document_repo = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global document_repo

    document_repo = DocumentRepository()
    yield


router = APIRouter(
    prefix="/feature-selection", tags=["Feature Selection"], lifespan=lifespan
)


class GetAllFeaturesRequestModel(BaseModel):
    doc_id: str


class GetAllFeaturesResponseModel(BaseModel):
    id: str
    text: Optional[str]
    selected: bool


@router.post("/get-all")
def get_all_features(
    item: GetAllFeaturesRequestModel,
) -> list[GetAllFeaturesResponseModel]:
    results = document_repo.get_all_features(doc_id=item.doc_id)
    print(results)
    return [GetAllFeaturesResponseModel(**result) for result in results]


@router.post("/set-features")
def set_features(item: list[GetAllFeaturesResponseModel]):
    for feature in item:
        document_repo.set_selected_feature(
            record_id=feature.id, selected=feature.selected
        )
    return {"message": "Done!"}
