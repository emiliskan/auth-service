# coding: utf-8
import uuid

from flask import Blueprint
from flask_jwt_extended import current_user, jwt_required
from flask import request, Response

from db import db
from .serializers import permission_schemas, permission_schema
from .models import Permission

blueprint = Blueprint('permissions', __name__, url_prefix='/permissions')


@blueprint.route('/', methods=('GET',), endpoint='get_permissions')
def get_permissions():
    """
    Список всех прав
    """
    permissions = Permission.query.all()
    return permission_schemas.dump(permissions)


@blueprint.route('/', methods=('POST',), endpoint='create_permission')
def create_permission():
    """
    Добавить право
    """
    permission_schema.load(request.data, session=db.session)
    return Response(status=200)


@blueprint.route('/<permission_id>', methods=('DELETE',), endpoint='delete_permission')
def delete_permission(permission_id: uuid):
    """
    Удалить право
    """
    Permission.query.delete(id=permission_id)
    return Response(status=200)
