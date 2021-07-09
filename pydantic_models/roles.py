import uuid

from pydantic import BaseModel
from typing import Optional


class RoleModel(BaseModel):
    id: Optional[str]
    name: str
    description: Optional[str]


class UserRoleModel(BaseModel):
    role_id: uuid.UUID
    user_id: uuid.UUID


class UserHasRoleModel(BaseModel):
    result: bool
