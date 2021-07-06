import uuid

from sqlalchemy.dialects.postgresql import UUID
from flask_security import UserMixin, SQLAlchemyUserDatastore, Security

from db import db
from role.models import Role, roles_users
from sqlalchemy.dialects.postgresql import JSON


class User(db.Model, UserMixin):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('user'))


class Result(db.Model):
    __tablename__ = 'result'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    result_all = db.Column(JSON)
    result_no_stop_words = db.Column(JSON)

    def __init__(self, url, result_all, result_no_stop_words):
        self.url = url
        self.result_all = result_all
        self.result_no_stop_words = result_no_stop_words

    def __repr__(self):
        return '<id {}>'.format(self.id)


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
# security = Security(app, user_datastore)
