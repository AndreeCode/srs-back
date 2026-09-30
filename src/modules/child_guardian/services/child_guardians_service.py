from .child_guardian_create_service import create
from .child_guardian_delete_service import delete
from .child_guardian_get_all_service import get_all
from .child_guardian_get_by_id_service import get_by_id
from .child_guardian_update_service import update


class ChildGuardianService:
    create = staticmethod(create)
    get_all = staticmethod(get_all)
    get_by_id = staticmethod(get_by_id)
    update = staticmethod(update)
    delete = staticmethod(delete)


childGuardianService = ChildGuardianService()
