import uuid

from config.app import db
from models import Permission


class PermissionService:
    """
    Сервис для управление правами
    """

    @staticmethod
    def get(permission_id: uuid) -> Permission:
        """
        Получение объекта в базе по идентификатору
        @param permission_id: Идентификатор необходимого объекта
        @return: Найденный объект
        """
        return Permission.query.get(permission_id)

    @staticmethod
    def create(permission: dict) -> Permission:
        """
        Создание права
        @param permission: dict с параметрами объекта
        @return: Созданный объект
        """
        new_permission = Permission(**permission)
        db.session.add(new_permission)
        db.session.commit()
        return new_permission

    @staticmethod
    def change(role_id: str, role_data: dict) -> Permission:
        """
        Изменение объекта в базе
        @param role_id: Идентификатор объекта
        @param role_data: dict с параметрами объекта
        @return: Измененный объект
        """
        role = PermissionService.get(role_id)
        role.update(**role_data)
        db.session.commit()
        return role

    @staticmethod
    def delete(permission_id: str) -> None:
        """
        Удаление объекта
        @param permission_id: Идентификатор объекта к удалению
        """
        Permission.query.filter_by(id=permission_id).delete()
        db.session.commit()

