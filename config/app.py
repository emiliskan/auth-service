"""The app module, containing the app factory function."""
from config.extentions import api, db, jwt, ma, migrate, user_datastore
from config.settings import Config
from flask import Flask
from flask_security import Security
from pydantic_models import RegistrationBodyModel, RoleModel, UserRoleModel
from services import create_role, create_user, create_user_role

settings = Config()
API_V1_PREFIX = "/api/v1"


def create_app(config_object=Config):
    app = Flask(__name__)

    # SQLAlchemy
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.SQLALCHEMY_DATABASE_URI

    # Flask Security
    app.config["SECRET_KEY"] = settings.SECRET_KEY
    app.config["SECURITY_PASSWORD_SALT"] = settings.SECURITY_PASSWORD_SALT

    # Flask-JWT
    app.config["JWT_SECRET_KEY"] = settings.JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = settings.JWT_ACCESS_TOKEN_EXPIRES
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = settings.JWT_REFRESH_TOKEN_EXPIRES
    app.url_map.strict_slashes = False
    app.config.from_object(config_object)

    # Register
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    Security(app=app, datastore=user_datastore, register_blueprint=False)
    jwt.init_app(app)
    api.register(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    from api.v1.role import role_blueprint
    from api.v1.user import auth_blueprint
    from api.v1.user_role import user_role_blueprint

    app.register_blueprint(auth_blueprint, url_prefix=API_V1_PREFIX)
    app.register_blueprint(role_blueprint, url_prefix=API_V1_PREFIX)
    app.register_blueprint(user_role_blueprint, url_prefix=API_V1_PREFIX)


def register_commands(app):
    @app.cli.command("create_super_user")
    def create_super_user():
        admin = create_user(
            RegistrationBodyModel(username=settings.admin_name, email="admin@a.com", password=settings.admin_pass)
        )

        role = create_role(RoleModel(name=settings.admin_role))

        create_user_role(UserRoleModel(user_id=str(admin.id), role_id=str(role.id)))
