import pytest
import pytest_cases

API_URL = "roles"


@pytest.mark.asyncio
async def test_roles(make_get_request):
    """
    Список всех ролей
    """
    response = await make_get_request(method=API_URL)
    assert response.status == status.HTTP_200_OK


@pytest_cases.parametrize(
    "http_status, params",
    [(status.HTTP_200_OK, {"role_name": "FILMS_READ"})],
)
@pytest.mark.asyncio
async def test_create_roles(http_status, params, make_get_request):
    """
    Создание роли
    """
    response = await make_get_request(method=API_URL, params=params)
    assert response.status == http_status


@pytest_cases.parametrize(
    'http_status, role_id, params',
    [(status.HTTP_200_OK, 'uuid', {'role_name': 'FILMS_READ'})],
)
@pytest.mark.asyncio
async def test_change_roles(http_status, role_id, params, make_post_request):
    """
    Изменение роли
    """
    response = await make_post_request(method=f'{API_URL}/{role_id}', params=params)
    assert response.status == http_status


@pytest_cases.parametrize(
    'http_status, role_id',
    [(status.HTTP_200_OK, 'uuid')],
)
@pytest.mark.asyncio
async def test_delete_roles(http_status, role_id, make_delete_request):
    """
    Удаление роли
    """
    response = await make_delete_request(method=f'{API_URL}/{role_id}')
    assert response.status == http_status
