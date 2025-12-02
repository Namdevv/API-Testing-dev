from typing import Optional

from sqlmodel import Session, select

from src.models import TestCaseReportModel
from src.settings import get_db_engine


class TestCaseReportRepository(TestCaseReportModel, table=True):
    """Repository for Test Case operations."""

    __tablename__ = "test_case_report"

    @classmethod
    def get_all_by_test_suite_report_id(
        cls,
        test_suite_report_id: str,
        session: Optional[Session] = None,
    ) -> list["TestCaseReportRepository"]:
        session = session or Session(get_db_engine())

        with session:
            statement = select(cls).where(
                cls.test_suite_report_id == test_suite_report_id
            )
            results = session.exec(statement).all()

        return results
