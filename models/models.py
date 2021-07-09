from config.database import db
from flask_security import RoleMixin, UserMixin
from models.mixins import PatchedUUID, TimedModel, UUIDModel
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import backref, relationship


class RolesUsers(UUIDModel):
    __tablename__ = "roles_users"

    user_id = Column("user_id", PatchedUUID(as_uuid=True), ForeignKey("user.id"))
    role_id = Column("role_id", PatchedUUID(as_uuid=True), ForeignKey("role.id"))

    def __repr__(self):
        return f'{self.user_id} {self.role_id}'


class RolesPermissions(UUIDModel):
    __tablename__ = 'roles_permissions'

    permission_id = Column('permission_id', PatchedUUID(as_uuid=True), ForeignKey('permission.id'))
    role_id = Column('role_id', PatchedUUID(as_uuid=True), ForeignKey('role.id'))

    def __repr__(self):
        return f'{self.permission_id} {self.role_id}'


class Role(UUIDModel, RoleMixin):
    __tablename__ = "role"

    name = Column(String(80), unique=True)
    description = Column(String(255), default='')

    permissions = relationship('Permission', secondary='roles_permissions',
                               backref=backref('roles', lazy='dynamic'))

    def __repr__(self):
        return f'{self.name} {self.description}'


class Permission(UUIDModel):
    name = Column(String(80), unique=True)
    description = Column(String(255), default='')

    def __repr__(self):
        return f'{self.name} {self.description}'


class User(TimedModel, UserMixin):
    __tablename__ = "user"

    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    active = db.Column(db.Boolean())

    token = relationship(
        "Token",
        secondary="user_history",
        backref=backref("tokens", lazy="dynamic"),
        cascade="all",
        passive_deletes=True,
    )

    roles = relationship("Role", secondary="roles_users", backref=backref("users", lazy="dynamic"))

    def __repr__(self):
        return f"<User username={self.username}>"


class Token(TimedModel):
    __tablename__ = "token"

    refresh_token = Column(String, nullable=False)


class UserHistory(TimedModel):
    __tablename__ = "user_history"

    user_id = Column("user_id", PatchedUUID(as_uuid=True), ForeignKey("user.id"))
    token_id = Column("token_id", PatchedUUID(as_uuid=True), ForeignKey("token.id"))
    user_agent = Column(String)
