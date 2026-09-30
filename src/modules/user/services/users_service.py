from .user_create_service import create
from .user_delete_service import delete
from .user_get_all_service import get_all
from .user_get_by_id_service import get_by_id
from .user_get_by_username_service import get_by_username
from .user_update_service import update


class UserService:
    create = staticmethod(create)
    get_all = staticmethod(get_all)
    get_by_id = staticmethod(get_by_id)
    get_by_username = staticmethod(get_by_username)
    update = staticmethod(update)
    delete = staticmethod(delete)


userService = UserService()
