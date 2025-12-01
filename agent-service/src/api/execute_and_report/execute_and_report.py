import uuid

from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from src import repositories
from src.models import StandardOutputModel
from src.services.test_case.execute_test_case import execute_test_suite

router = APIRouter(prefix="/execute-and-report", tags=["Execution and Reporting"])


class ExecuteTestSuiteModel(BaseModel):
    test_suite_id: str


@router.post("/execute")
async def execute_test_suite_api(
    items: ExecuteTestSuiteModel, background_tasks: BackgroundTasks
) -> StandardOutputModel:

    test_suite_report_id = str(uuid.uuid4())
    background_tasks.add_task(
        execute_test_suite,
        test_suite_report_id=test_suite_report_id,
        test_suite_id=items.test_suite_id,
    )
    response = StandardOutputModel(
        result={
            "code": ["0000"],
            "description": "Work in progress!",
        },
        data={
            "test_suite_report_id": test_suite_report_id,
        },
    )
    return response


class GetTestSuiteReportModel(BaseModel):
    test_suite_report_id: str


@router.get("/report/{test_suite_report_id}")
def get_test_suite_report(test_suite_report_id: str) -> StandardOutputModel:

    data = repositories.TestCaseReportRepository.get_all_by_test_suite_report_id(
        test_suite_report_id=test_suite_report_id
    )
    response = StandardOutputModel(
        result={
            "code": ["0000"],
            "description": "Report fetched successfully.",
        },
        data=data,
    )
    return response
