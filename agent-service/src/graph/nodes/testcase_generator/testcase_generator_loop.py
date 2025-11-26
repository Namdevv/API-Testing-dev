from src.models import TestcasesGenStateModel


def testcase_generator_loop(state: TestcasesGenStateModel) -> str:
    all_fr_groups = state.all_fr_groups

    if not all_fr_groups:
        return "completed"
    else:
        return "in_progress"
