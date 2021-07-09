from http import HTTPStatus

from flask import Blueprint
from flask import request
from flask_pydantic_spec import Response

from config.extentions import api
from services import user_has_role, create_user_role, delete_user_role
from services.pydantic import ResponseError
from services.utils import user_is_admin
from pydantic_models import UserRoleModel, UserHasRoleModel

user_role_blueprint = Blueprint('user_roles', __name__)


@user_role_blueprint.route('/user/role', methods=['GET'])
@user_is_admin
@api.validate(body=UserRoleModel, resp=Response(HTTP_200=UserHasRoleModel), tags=["UserRole"])
def check_user_role() -> dict:
    """Наличие роли у пользователя."""
    has_role = user_has_role(UserRoleModel.parse_raw(request.data))
    return {"result": has_role}


@user_role_blueprint.route('/user/role', methods=['POST'])
@user_is_admin
@api.validate(body=UserRoleModel, resp=Response(HTTP_200=None), tags=["UserRole"])
def set_role_user() -> dict:
    """Установить роль пользователю."""
    create_user_role(UserRoleModel.parse_raw(request.data))
    return ResponseError(code=HTTPStatus.OK, message="Role has been set.").dict()


@user_role_blueprint.route('/user/role', methods=['DELETE'])
@user_is_admin
@api.validate(body=UserRoleModel, resp=Response(HTTP_200=None), tags=["UserRole"])
def take_user_role() -> dict:
    """Удаление роли у пользователя."""
    result = delete_user_role(UserRoleModel.parse_raw(request.data))
    if not result:
        return ResponseError(code=HTTPStatus.NOT_FOUND, message="There is no user role with given ids.").dict()
    return ResponseError(code=HTTPStatus.OK, message="Role deleted from user.").dict()
