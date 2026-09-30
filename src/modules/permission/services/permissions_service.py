from .permission_create_service import create
from .permission_delete_service import delete
from .permission_get_all_service import get_all
from .permission_get_by_id_service import get_by_id
from .permission_update_service import update
from .permission_user_has_service import user_has


class PermissionService:
    create = staticmethod(create)
    get_all = staticmethod(get_all)
    get_by_id = staticmethod(get_by_id)
    update = staticmethod(update)
    delete = staticmethod(delete)
    user_has = staticmethod(user_has)


permissionService = PermissionService()
