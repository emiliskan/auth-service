import uuid

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LoginBodyModel(BaseModel):
    username: str
    password: str


class RegistrationBodyModel(LoginBodyModel):
    email: str


class InfoUpdateBodyModel(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    email: Optional[str]  # TODO: crutch. update via phone number.
    username: Optional[str]  # TODO: crutch. update via email.


class UserHistoryModel(BaseModel):
    id: str
    user_agent: str
    created_at: datetime
    updated_at: datetime
