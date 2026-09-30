from .child_guardian_create_repository import create_child_guardian
from .child_guardian_delete_repository import delete_child_guardian
from .child_guardian_get_all_repository import get_all_child_guardians
from .child_guardian_get_by_id_repository import get_child_guardian_by_id
from .child_guardian_update_repository import update_child_guardian


class ChildGuardianRepository:
    create = staticmethod(create_child_guardian)
    get_all = staticmethod(get_all_child_guardians)
    get_by_id = staticmethod(get_child_guardian_by_id)
    update = staticmethod(update_child_guardian)
    delete = staticmethod(delete_child_guardian)


childGuardianRepository = ChildGuardianRepository()
