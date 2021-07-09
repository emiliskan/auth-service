from config.app import db
from models import Role, RolesUsers
from pydantic_models import UserRoleModel


def get_user_roles(user_id: str) -> list[Role]:
    """
    Все роли пользователя
    @param user_id: Идентификатор пользователя
    @return: список ролей пользователя
    """
    return db.session.query(Role.name).join(RolesUsers).filter(RolesUsers.user_id == user_id).all()


def user_has_role(user_role: UserRoleModel) -> bool:
    """
    Проверка наличия роли у пользователя
    @param user_role: Объект модели с заполненными user_id и role_id
    @return: Признак наличия роли у пользователя
    """
    return len(RolesUsers.query.filter(
        RolesUsers.user_id == user_role.user_id,
        RolesUsers.role_id == user_role.role_id).all()) > 0


def create_user_role(user_role: UserRoleModel) -> None:
    """
    Добавить роль пользователю
    @param user_role: Объект модели с заполненными user_id и role_id
    @return: None
    """
    user_role = RolesUsers(user_id=user_role.user_id, role_id=user_role.role_id)
    db.session.add(user_role)
    db.session.commit()


def delete_user_role(user_role) -> bool:
    """
    Удалить роль пользователя
    @param user_role: Объект модели с заполненными user_id и role_id
    @return: если объект не найден, то возвращается false
    """
    user_roles = RolesUsers.query.filter_by(user_id=user_role.user_id, role_id=user_role.role_id)
    if len(user_roles.all()) == 0:
        return False

    user_roles.delete()
    db.session.commit()
    return True
