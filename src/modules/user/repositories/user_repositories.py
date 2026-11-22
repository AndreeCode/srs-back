from .user_create_repository import create_user
from .user_delete_repository import delete_user
from .user_get_all_repository import get_all_users
from .user_get_by_id_repository import get_user_by_id
from .user_get_by_username_repository import get_user_by_username
from .user_login_lock_repository import (
    get_user_locked_until,
    register_user_login_failure,
    reset_user_login_failures,
    set_user_password,
)
from .user_rehash_password_repository import rehash_user_password
from .user_update_repository import update_user


class UserRepository:
    create = staticmethod(create_user)
    get_all = staticmethod(get_all_users)
    get_by_id = staticmethod(get_user_by_id)
    get_by_username = staticmethod(get_user_by_username)
    update = staticmethod(update_user)
    delete = staticmethod(delete_user)
    rehash_password = staticmethod(rehash_user_password)
    locked_until = staticmethod(get_user_locked_until)
    register_login_failure = staticmethod(register_user_login_failure)
    reset_login_failures = staticmethod(reset_user_login_failures)
    set_password = staticmethod(set_user_password)


userRepository = UserRepository()
