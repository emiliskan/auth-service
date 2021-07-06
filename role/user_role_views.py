# coding: utf-8
from flask import Blueprint
from flask_jwt_extended import current_user, jwt_required

blueprint = Blueprint('user_roles', __name__)


@blueprint.route('/?user_id=<user_id>&role_id=<role_id>', methods=('GET',), endpoint='get_users')
@jwt_required
def get(self, user_id: str, role_id: str):
    """
    Наличие роли у пользователя
    """


@blueprint.route('/?user_id=<user_id>&role_id=<role_id>', methods=('GET',), endpoint='set_role')
@jwt_required
def post(self, user_id: str, role_id: str):
    """
    Установить роль пользователю
    """


@blueprint.route('/?user_id=<user_id>&role_id=<role_id>', methods=('DElETE',), endpoint='take_role')
@jwt_required
def delete(self, user_id: str, role_id: str):
    """
    Удалить роль пользователя
    """
