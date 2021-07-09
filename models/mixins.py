import uuid
from datetime import datetime

from config.database import db
from pydantic import validator
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID


class PatchedUUID(UUID):
    @property
    def python_type(self):
        return uuid.UUID


class UUIDModel(db.Model):
    __abstract__ = True

    id = Column(PatchedUUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    @validator("id")
    def validate_id(cls, value):
        return str(value)


class TimedModel(UUIDModel):
    __abstract__ = True

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
