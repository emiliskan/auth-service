from datetime import timedelta

from pydantic import BaseSettings, Field


class Config(BaseSettings):
    csrf_enabled = True
    debug = Field(False, env="DEBUG")
    flask_host = Field("0.0.0.0", env="FLASK_HOST")
    flask_port = Field(5000, env="FLASK_PORT")
    redis_host = Field("localhost", env="REDIS_HOST")
    redis_port = Field(6379, env="REDIS_PORT")

    postgres_host = Field("0.0.0.0", env="POSTGRES_HOST")
    postgres_port = Field(5432, env="POSTGRES_PORT")
    postgres_user = Field("postgres", env="POSTGRES_USER")
    postgres_pass = Field("", env="POSTGRES_PASSWORD")
    postgres_db_name = Field("postgres", env="POSTGRES_DB_NAME")

    SQLALCHEMY_DATABASE_URI = Field(
        f"postgresql://postgres:a82c4b82-5dbc-44f8-8fdb-160594057358@localhost:15433/postgres",
        env="SQLALCHEMY_DATABASE_URI",
    )
    secret_key = "watlol"

    # Flask-JWT
    JWT_SECRET_KEY = Field("CHANGE_ME_JWT_SECRET_KEY", env="JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = Field(timedelta(hours=10))
    JWT_REFRESH_TOKEN_EXPIRES = Field(timedelta(days=30))

    # Flask Security
    SECRET_KEY = Field("SECRET_KEY", env="SECRET_KEY")
    SECURITY_PASSWORD_SALT = Field("SECURITY_PASSWORD_SALT", env="SECURITY_PASSWORD_SALT")

    # Super user
    admin_name = Field("admin", env="ADMIN_NAME")
    admin_pass = Field("admin_pass", env="ADMIN_PASS")

    admin_role = "admin"
