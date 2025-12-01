import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field, Session, SQLModel, select

from src import repositories
from src.settings import get_db_engine, get_now_vn


class TestSuiteRepository(SQLModel, table=True):
    """Repository for Test Suite operations."""

    __tablename__ = "test_suite"

    test_suite_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Test Suite ID, must be unique.",
        max_length=64,
        primary_key=True,
    )

    fr_info_id: str = Field(
        description="document fr info external ID, must be unique.",
        max_length=64,
        foreign_key="document_fr_info.fr_info_id",
        # unique=True,
    )

    test_suite_name: str = Field(
        description="Name of the test suite.",
        max_length=256,
    )

    created_at: datetime = Field(
        default_factory=get_now_vn,
        description="Creation timestamp",
    )

    @classmethod
    def get_all_by_project_id(
        cls,
        project_id: str,
        session: Optional[Session] = None,
    ) -> list["TestSuiteRepository"]:
        session = session or Session(get_db_engine())

        with session:

            statement = (
                select(cls)
                .join(
                    repositories.DocumentFRInfoRepository,
                    cls.fr_info_id == repositories.DocumentFRInfoRepository.fr_info_id,
                )
                .join(
                    repositories.ProjectRepository,
                    repositories.DocumentFRInfoRepository.project_id
                    == repositories.ProjectRepository.project_id,
                )
                .where(repositories.ProjectRepository.project_id == project_id)
                .order_by(cls.created_at.desc())
            )
            results = session.exec(statement).all()
            return results
