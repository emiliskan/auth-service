import uuid
from typing import Optional

from config.app import db
from models import Role
from pydantic_models import RoleModel


def get_role(role_id: uuid.UUID) -> Role:
    """
    Получение объекта в базе
    @param role_id: Идентификатор необходимого объекта
    @return: Найденный объект
    """
    return Role.query.get(role_id)


def get_roles() -> list[Role]:
    """
    Получение списка всех ролей
    @return: Массив всех ролей
    """
    return Role.query.all()


def create_role(body: RoleModel) -> Role:
    """
    Создание роли
    @param body: pydantic модель роли
    @return: Созданный объект
    """
    new_role = Role(**body.dict())
    db.session.add(new_role)
    db.session.commit()
    return new_role


def change_role(role_id: uuid.UUID, body: RoleModel) -> Optional[Role]:
    """
    Изменение объекта в базе
    @param body: pydantic модель роли
    @param role_id: Идентификатор объекта
    @return: Измененный объект или None если объект не найден
    """
    role = get_role(role_id)
    if not role:
        return
    role.update(**body.dict(exclude_none=True))
    db.session.commit()
    return role


def delete_role(role_id: uuid.UUID) -> bool:
    """
    Удаление объекта
    @param role_id: Идентификатор объекта к удалению
    """
    role = get_role(role_id)

    if not role:
        return False

    role.delete()
    db.session.commit()
    return True
