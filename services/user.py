import uuid
from http import HTTPStatus

from config.extentions import db, user_datastore
from models import Token, User, UserHistory
from services.pydantic import ResponseError
from werkzeug.security import check_password_hash, generate_password_hash

from .utils import generate_tokens, identify_user, remove_redis_access


def create_user(body) -> User:
    user = user_datastore.create_user(
        username=body.username,
        email=body.email,
        password=generate_password_hash(body.password),
    )
    db.session.commit()
    return user


def register_user(body) -> dict:
    user = create_user(body)
    token_pair, token_instance = generate_tokens(user.id)
    user.token = [token_instance]
    return token_pair


def login(body) -> dict:
    user = user_datastore.find_user(username=body.username)
    if not user and check_password_hash(user.password, body.password):
        ResponseError(code=HTTPStatus.BAD_REQUEST, message="Login or password is incorrect.").abort()

    token_data, token_instance = generate_tokens(user.id)
    user_history = UserHistory(user_id=user.id, token_id=token_instance.id)
    db.session.add(user_history)
    db.session.commit()
    return token_data


def logout() -> dict:
    """Set access token to blacklist and delete refresh."""
    _, token_id, token_jti = identify_user()
    refresh_token = Token.query.get(token_id)

    if refresh_token:
        db.session.delete(refresh_token)
        db.session.commit()

    remove_redis_access(token_jti)


def get_user_info() -> dict:
    user_id, *_ = identify_user()
    return User.query.get(user_id)


def update_user_info(body) -> None:
    user_id, *_ = identify_user()
    User.query.filter_by(id=user_id).update(body.dict(exclude_none=True))
    db.session.commit()


def get_user_history():
    user_id, *_ = identify_user()
    return db.session.query(UserHistory).filter_by(user_id=user_id).all()


def delete_user_history(token_id_to_delete: uuid.UUID) -> bool:
    user_id, *_ = identify_user()
    token_history = UserHistory.query.filter_by(id=token_id_to_delete, user_id=user_id).first()

    if not token_history:
        return False

    db.session.delete(Token.query.get(token_history.token_id))
    db.session.commit()
    return True
