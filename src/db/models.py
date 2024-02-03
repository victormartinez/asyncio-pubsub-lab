import uuid

from sqlalchemy import (
    Column,
    String,
)
from sqlalchemy.dialects import postgresql
from src.db import BaseModel


class Person(BaseModel):
    __tablename__ = "persons"

    id = Column(
        postgresql.UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    name = Column(String, index=True, nullable=False)
