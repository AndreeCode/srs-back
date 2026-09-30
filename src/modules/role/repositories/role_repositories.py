from .role_create_repository import create_role
from .role_delete_repository import delete_role
from .role_get_all_repository import get_all_roles
from .role_get_by_id_repository import get_role_by_id
from .role_update_repository import update_role


class RoleRepository:
    create = staticmethod(create_role)
    get_all = staticmethod(get_all_roles)
    get_by_id = staticmethod(get_role_by_id)
    update = staticmethod(update_role)
    delete = staticmethod(delete_role)


roleRepository = RoleRepository()
