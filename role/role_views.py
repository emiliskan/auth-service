# coding: utf-8
import uuid

from flask import Blueprint
from flask_jwt_extended import current_user, jwt_required
from flask import request, Response

from db import db
from .models import Role
from .serializers import role_schemas, role_schema

blueprint = Blueprint('roles', __name__)


@blueprint.route('/', methods=('GET',), endpoint='get_roles')
def get_roles():
    """
    Список всех ролей
    """
    roles = Role.query.all()
    return role_schemas.dump(roles)


@blueprint.route('/', methods=('POST',), endpoint='create_role')
def create_role():
    """
    Создание роли
    """
    role_schema.load(request.data, session=db.session)
    return Response(status=200)


@blueprint.route('/<role_id>', methods=('POST',), endpoint='change_role')
def change_role(role_id: uuid):
    """
    Изменение роли
    """
    role = Role.query.get(role_id)
    role_schema.load(request.data, session=db.session)
    return Response(status=200)


@blueprint.route('/<role_id>', methods=('DELETE',), endpoint='delete_role')
def delete_role(role_id: uuid):
    """
    Удаление роли
    """
    Role.query.delete(id=role_id)
    return Response(status=200)
