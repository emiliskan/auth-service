"""Extensions module. Each extension is initialized in the app factory located in app.py."""

from config.database import db

from flasgger import Swagger
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_pydantic_spec import FlaskPydanticSpec
from flask_security import SQLAlchemyUserDatastore

from models.models import Role, User
from redis import Redis

migrate = Migrate()
ma = Marshmallow()
redis = Redis()
db = db
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
api = FlaskPydanticSpec("flask")

jwt = JWTManager()
