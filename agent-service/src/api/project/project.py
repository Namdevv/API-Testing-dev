from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src import repositories

router = APIRouter(prefix="/project", tags=["Project"])


class CreateProjectResponseModel(BaseModel):
    project_id: str


@router.post("/create")
def create_project(
    project: repositories.ProjectRepository,
) -> CreateProjectResponseModel:

    project = project.create()
    return CreateProjectResponseModel(project_id=project.project_id)


@router.get("/all/{user_id}")
def get_all_projects(user_id: str) -> list[repositories.ProjectRepository]:
    projects = repositories.ProjectRepository().get_all(user_id=user_id)
    return projects


@router.post("/delete/{project_id}")
def delete_project(project_id: str) -> None:
    if repositories.ProjectRepository.delete_by_id(project_id):
        return {"message": "Project deleted successfully"}

    raise HTTPException(status_code=400, detail="Project not found")
