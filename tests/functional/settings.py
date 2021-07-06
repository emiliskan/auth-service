import os
from pathlib import Path

from pydantic import BaseSettings, Field

BASE_DIR = Path(__file__).resolve().parent


class TestSettings(BaseSettings):
    redis_host = Field("localhost", env="REDIS_HOST")
    redis_port = Field("6379", env="REDIS_PORT")
    api_host = Field("localhost", env="BACKEND_API_HOST")
    api_port = Field("8000", env="BACKEND_API_PORT")
    base_dir = Field(BASE_DIR, env="BASE_DIR", description="Путь к корневой папке тестов.")
    test_data_dir = Field(
        os.path.join(BASE_DIR, "testdata"),
        description="Путь к папке данных.",
    )
