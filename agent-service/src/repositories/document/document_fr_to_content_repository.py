import uuid
from typing import Optional

from pydantic import (
    ConfigDict,
)
from sqlmodel import Field, Session, SQLModel, select

from src.settings import get_db_engine


class DocumentFRToContentRepository(SQLModel, table=True):
    __tablename__ = "document_fr_to_content"

    fr_to_content_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="unique ID for the document fr to content mapping",
        max_length=64,
        primary_key=True,
    )

    fr_info_id: str = Field(
        description="document fr info external ID",
        max_length=64,
        foreign_key="document_fr_info.fr_info_id",
    )

    content_id: str = Field(
        description="content ID",
        max_length=64,
        foreign_key="document_content.content_id",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "fr_info_id": "123e4567-e89b-12d3-a456-426614174000",
                "content_id": "asdf1234-asdf-1234-asdf-1234asdf1234",
            }
        }
    )

    @classmethod
    def delete_by_fr_info_id(
        cls, fr_info_id: str, session: Optional[Session] = None
    ) -> bool:

        session = session or Session(get_db_engine())
        with session:
            fr_to_contents = session.exec(
                select(cls).where(cls.fr_info_id == fr_info_id)
            ).all()
            for fr_to_content in fr_to_contents:
                session.delete(fr_to_content)
            session.commit()

            return True
        return False
