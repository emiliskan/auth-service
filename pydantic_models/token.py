
from pydantic import BaseModel


class RefreshTokenModel(BaseModel):
    refresh_token: str


class AccessTokenModel(BaseModel):
    access_token: str


class PairTokenModel(RefreshTokenModel, AccessTokenModel):
    ...
