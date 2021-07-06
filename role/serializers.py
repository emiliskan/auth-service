from marshmallow import Schema, fields
from .models import Role, Permission
from ma import ma


class PermissionSchema(ma.SQLAlchemySchema):
    name = fields.Str()

    class Meta:
        strict = True
        model = Permission


class RoleSchema(ma.SQLAlchemySchema):
    name = fields.Str()
    # permissions = fields.List(cls_or_instance=PermissionSchema)

    class Meta:
        strict = True
        model = Role


role_schema = RoleSchema()
role_schemas = RoleSchema(many=True)

permission_schema = PermissionSchema()
permission_schemas = PermissionSchema(many=True)
