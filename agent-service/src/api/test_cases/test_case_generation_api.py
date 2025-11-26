from fastapi import APIRouter

from src.graph.workflows import TestCaseGenerationWorkflow
from src.models import TestcasesGenStateModel

router = APIRouter(prefix="/test-case", tags=["Test Case"])


@router.post("/generate-test-cases")
def docs_preprocessing(
    item: TestcasesGenStateModel,
) -> TestcasesGenStateModel:
    workflow = TestCaseGenerationWorkflow()

    result = workflow.invoke(item)
    return result
