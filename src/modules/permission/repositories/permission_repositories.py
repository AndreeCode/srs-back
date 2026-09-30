from .permission_create_repository import create_permission
from .permission_delete_repository import delete_permission
from .permission_get_all_repository import get_all_permissions
from .permission_get_by_id_repository import get_permission_by_id
from .permission_update_repository import update_permission
from .permission_user_has_repository import user_has_permission


class PermissionRepository:
    create = staticmethod(create_permission)
    get_all = staticmethod(get_all_permissions)
    get_by_id = staticmethod(get_permission_by_id)
    update = staticmethod(update_permission)
    delete = staticmethod(delete_permission)
    user_has = staticmethod(user_has_permission)


permissionRepository = PermissionRepository()
