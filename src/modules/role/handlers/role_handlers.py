from .role_create_handler import create_role_handler
from .role_delete_handler import delete_role_handler
from .role_get_all_handler import get_all_roles_handler
from .role_get_by_id_handler import get_role_by_id_handler
from .role_update_handler import update_role_handler


class RoleHandler:
    create = staticmethod(create_role_handler)
    get_all = staticmethod(get_all_roles_handler)
    get_by_id = staticmethod(get_role_by_id_handler)
    update = staticmethod(update_role_handler)
    delete = staticmethod(delete_role_handler)


roleHandler = RoleHandler()
