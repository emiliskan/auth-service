import uuid
from http import HTTPStatus

from config.extentions import api
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from flask_pydantic_spec import Response
from models import User, UserHistory
from pydantic_models import (
    InfoUpdateBodyModel,
    LoginBodyModel,
    PairTokenModel,
    RegistrationBodyModel,
    UserHistoryModel,
)
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from services import (
    delete_user_history,
    get_user_history,
    get_user_info,
    login,
    logout,
    register_user,
    update_refresh_token,
    update_user_info,
)
from services.pydantic import ResponseError
from services.utils import response_json_list

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/user/registration", methods=["POST"])
@api.validate(body=RegistrationBodyModel, resp=Response(HTTP_201=PairTokenModel), tags=["User"])
def registration() -> dict:
    return register_user(RegistrationBodyModel.parse_raw(request.data))


@auth_blueprint.route("/user/login", methods=["POST"])
@api.validate(body=LoginBodyModel, resp=Response(HTTP_200=PairTokenModel), tags=["User"])
def user_login():
    return login(LoginBodyModel.parse_raw(request.data))


@auth_blueprint.route("/user/logout", methods=["POST"])
@jwt_required()
@api.validate(resp=Response(HTTP_200=ResponseError), tags=["User"])
def user_logout() -> dict:
    logout()
    return ResponseError(code=HTTPStatus.OK, message="Logout is success.").dict()


@auth_blueprint.route("user/info", methods=["GET"])
@jwt_required()
@api.validate(resp=Response(HTTP_200=InfoUpdateBodyModel), tags=["User"])
def info_get() -> dict:
    return sqlalchemy_to_pydantic(User).from_orm(get_user_info()).dict()


@auth_blueprint.route("/user/info", methods=["PUT"])
@jwt_required()
@api.validate(body=InfoUpdateBodyModel, resp=Response(HTTP_200=InfoUpdateBodyModel), tags=["User"])
def info_update() -> dict:
    body = InfoUpdateBodyModel.parse_raw(request.data)
    update_user_info(body)
    return body.dict(exclude_none=True)


@auth_blueprint.route("/user/history", methods=["GET"])
@jwt_required()
@api.validate(resp=Response(HTTP_200=UserHistoryModel, validate=False), tags=["User"])
@response_json_list
def history_get() -> list:
    qs = get_user_history()
    model = sqlalchemy_to_pydantic(UserHistory)
    return [model.from_orm(obj).dict() for obj in qs]


@auth_blueprint.route("/user/history/<uuid:token_id>", methods=["DELETE"])
@jwt_required()
@api.validate(resp=Response(HTTP_200=ResponseError), tags=["User"])
def history_delete(token_id: uuid.UUID) -> dict:
    result = delete_user_history(token_id)
    if not result:
        return ResponseError(code=HTTPStatus.NOT_FOUND, message="Session token not found.").dict()

    return ResponseError(code=HTTPStatus.OK, message="Session deleted successfully.").dict()


@auth_blueprint.route("/user/token/refresh", methods=["POST"])
@jwt_required(refresh=True)
@api.validate(resp=Response(HTTP_200=PairTokenModel), tags=["User"])
def refresh() -> dict:
    token_pair = update_refresh_token()
    if not token_pair:
        return ResponseError(code=HTTPStatus.NOT_FOUND, message="Refresh-token is not found.").dict()
    return token_pair
