from .user_create_handler import create_user_handler
from .user_delete_handler import delete_user_handler
from .user_get_all_handler import get_all_users_handler
from .user_get_by_id_handler import get_user_by_id_handler
from .user_update_handler import update_user_handler


class UserHandler:
    create = staticmethod(create_user_handler)
    get_all = staticmethod(get_all_users_handler)
    get_by_id = staticmethod(get_user_by_id_handler)
    update = staticmethod(update_user_handler)
    delete = staticmethod(delete_user_handler)


userHandler = UserHandler()
