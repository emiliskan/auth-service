import uuid
from sqlalchemy.dialects.postgresql import UUID
from flask_security import RoleMixin
from db import db

roles_users = db.Table('roles_users',
                       db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('user.id')),
                       db.Column('role_id', UUID(as_uuid=True), db.ForeignKey('role.id')))

roles_permissions = db.Table('roles_permissions',
                             db.Column('role_id', UUID(as_uuid=True), db.ForeignKey('role.id')),
                             db.Column('permissions_id', UUID(as_uuid=True), db.ForeignKey('permissions.id')))


class Permission(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String())
    description = db.Column(db.String())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<id {self.name}>'


class Role(db.Model, RoleMixin):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(80), unique=True)
    permissions = db.relationship('Permission', secondary=roles_permissions, backref=db.backref('role'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<{self.role_name}>'

