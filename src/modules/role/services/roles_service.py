from .role_create_service import create
from .role_delete_service import delete
from .role_get_all_service import get_all
from .role_get_by_id_service import get_by_id
from .role_update_service import update


class RoleService:
    create = staticmethod(create)
    get_all = staticmethod(get_all)
    get_by_id = staticmethod(get_by_id)
    update = staticmethod(update)
    delete = staticmethod(delete)


roleService = RoleService()
