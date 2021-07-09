import uuid
from http import HTTPStatus

from config.extentions import api
from flask import Blueprint, request
from flask_pydantic_spec import Response
from models import Role
from pydantic_models import RoleModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from services import change_role, create_role, delete_role, get_roles
from services.pydantic import ResponseError
from services.utils import response_json_list, user_is_admin

role_blueprint = Blueprint("roles", __name__)


@role_blueprint.route("/roles", methods=["GET"])
@user_is_admin
@api.validate(resp=Response(HTTP_200=RoleModel, validate=False), tags=["Role"])
@response_json_list
def get_all() -> list:
    """Получить все роли."""
    qs = get_roles()
    model = sqlalchemy_to_pydantic(Role)
    return [model.from_orm(obj).dict() for obj in qs]


@role_blueprint.route("/roles", methods=["POST"])
@user_is_admin
@api.validate(body=RoleModel, resp=Response(HTTP_201=RoleModel), tags=["Role"])
def create() -> dict:
    """Создание роли."""
    new_role = create_role(RoleModel.parse_raw(request.data))
    return sqlalchemy_to_pydantic(Role).from_orm(new_role).dict()


@role_blueprint.route("/roles/<uuid:role_id>", methods=["PUT"])
@user_is_admin
@api.validate(body=RoleModel, resp=Response(HTTP_200=RoleModel), tags=["Role"])
def change(role_id: uuid.UUID) -> dict:
    """Изменение роли."""
    changed_role = change_role(role_id, RoleModel.parse_raw(request.data))
    if not changed_role:
        return ResponseError(code=HTTPStatus.NOT_FOUND, message="Role not found.").dict()

    return sqlalchemy_to_pydantic(Role).from_orm(changed_role).dict()


@role_blueprint.route("/roles/<uuid:role_id>", methods=["DELETE"])
@user_is_admin
@api.validate(resp=Response(HTTP_200=ResponseError), tags=["Role"])
def delete(role_id: uuid.UUID) -> dict:
    """Удаление роли."""
    result = delete_role(role_id)
    if not result:
        return ResponseError(code=HTTPStatus.NOT_FOUND, message="Role not found.").dict()

    return ResponseError(code=HTTPStatus.OK, message="Role deleted.").dict()
