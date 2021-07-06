from pydantic import BaseSettings, Field


class Config(BaseSettings):
    csrf_enabled = True
    debug = Field(False, env="DEBUG")
    flask_host = Field("0.0.0.0", env="FLASK_HOST")
    flask_port = Field(5000, env="FLASK_PORT")
    postgres_host = Field("postgres_auth", env="POSTGRES_HOST")
    postgres_port = Field(5432, env="POSTGRES_PORT")
    postgres_user = Field("postgres", env="POSTGRES_USER")
    postgres_pass = Field("", env="POSTGRES_PASSWORD")
    postgres_db_name = Field("postgres", env="POSTGRES_DB_NAME")

    redis_host = Field("redis_auth", env="REDIS_HOST")
    redis_port = Field(6379, env="REDIS_PORT")
    SQLALCHEMY_DATABASE_URI = Field(
        f"postgresql://{postgres_user}:{postgres_pass}@{postgres_host}:{postgres_port}/{postgres_db_name}",
        env="SQLALCHEMY_DATABASE_URI"
    )
    secret_key = "watlol"
