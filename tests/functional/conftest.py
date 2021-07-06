import json
import os
import requests
from dataclasses import dataclass

import backoff
import pytest
from multidict import CIMultiDictProxy
from tests.functional.settings import TestSettings

test_settings = TestSettings()


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope="session")
def settings() -> TestSettings:
    return TestSettings()


@pytest.fixture(scope="session")
def session():
    session = requests.session()
    yield session
    session.close()


@pytest.fixture(scope="session")
def make_get_request(session, settings):
    # Here can be million errors:
    # Socket error
    # Redis error
    # Elastic error
    # Validation error
    # Actually I need to choose only necessary but for demo purpose it's fine.
    @backoff.on_exception(backoff.expo, Exception, max_tries=10)
    async def inner(method: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        url = f"http://{settings.api_host}:{settings.api_port}/v1/{method}"
        with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture(scope="session")
def make_post_request(session, settings):
    @backoff.on_exception(backoff.expo, Exception, max_tries=10)
    async def inner(method: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        url = f"http://{settings.api_host}:{settings.api_port}/v1/{method}"
        with session.post(url, params=params) as response:
            return HTTPResponse(
                body=response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture(scope="session")
def make_delete_request(session, settings):

    @backoff.on_exception(backoff.expo, Exception, max_tries=10)
    async def inner(method: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        url = f"http://{settings.api_host}:{settings.api_port}/v1/{method}"
        with session.delete(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture(autouse=True, scope="session")
async def init_data(es_client):
    indices = [
        (
        ),
    ]

    for index_params in indices:
        pass
