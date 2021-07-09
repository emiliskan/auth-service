import json
import uuid
from functools import wraps
from http import HTTPStatus

from common.utils import CustomEncoder
from config.extentions import db, redis
from config.settings import Config
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    jwt_required,
)
from models import Token
from services.pydantic import ResponseError
from services.user_role import get_user_roles

settings = Config()


def generate_tokens(user_id: str) -> tuple[dict, Token]:
    """Generate access and refresh tokens."""
    token_id = uuid.uuid4()
    roles = [role[0] for role in get_user_roles(user_id)]
    payload = {"user_id": user_id, "roles": roles}
    access_token = create_access_token(identity=token_id, additional_claims=payload)
    refresh_token = create_refresh_token(identity=token_id, additional_claims=payload)

    token = Token(id=token_id, refresh_token=refresh_token)
    db.session.add(token)
    db.session.flush()
    db.session.commit()
    return {"access_token": access_token, "refresh_token": refresh_token}, token


def identify_user() -> tuple[str, str, str]:
    """Get data from access jwt token."""
    jwt_access = get_jwt()
    token_id: str = jwt_access["sub"]
    user_id: str = jwt_access["user_id"]
    redis_jti: str = jwt_access["jti"]
    return user_id, token_id, redis_jti


def remove_redis_access(jti: str) -> None:
    """Set refresh token to block list."""
    redis.set(jti, "", ex=settings.JWT_ACCESS_TOKEN_EXPIRES)


def user_is_admin(func):
    @wraps(func)
    @jwt_required()
    def wrapper(*args, **kwargs):
        jwt_access = get_jwt()
        roles = jwt_access["roles"]
        if settings.admin_role not in roles:
            return ResponseError(code=HTTPStatus.METHOD_NOT_ALLOWED, message="Only admin can do this").abort()
        return func(*args, **kwargs)

    return wrapper


def response_json_list(func):
    @wraps(func)
    def wrapper(*args, **kwargs) -> str:
        return json.dumps(func(*args, **kwargs), cls=CustomEncoder)

    return wrapper
