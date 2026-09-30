from .permission_create_handler import create_permission_handler
from .permission_delete_handler import delete_permission_handler
from .permission_get_all_handler import get_all_permissions_handler
from .permission_get_by_id_handler import get_permission_by_id_handler
from .permission_update_handler import update_permission_handler


class PermissionHandler:
    create = staticmethod(create_permission_handler)
    get_all = staticmethod(get_all_permissions_handler)
    get_by_id = staticmethod(get_permission_by_id_handler)
    update = staticmethod(update_permission_handler)
    delete = staticmethod(delete_permission_handler)


permissionHandler = PermissionHandler()
