from .user import (
    history_delete,
    history_get,
    info_get,
    info_update,
    refresh,
    registration,
    user_login,
    user_logout,
)

auth_api = [registration, refresh, history_delete, history_get, user_login, user_logout, info_get, info_update]
