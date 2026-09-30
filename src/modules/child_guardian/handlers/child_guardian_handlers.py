from .child_guardian_create_handler import create_child_guardian_handler
from .child_guardian_delete_handler import delete_child_guardian_handler
from .child_guardian_get_all_handler import get_all_child_guardians_handler
from .child_guardian_get_by_id_handler import get_child_guardian_by_id_handler
from .child_guardian_update_handler import update_child_guardian_handler


class ChildGuardianHandler:
    create = staticmethod(create_child_guardian_handler)
    get_all = staticmethod(get_all_child_guardians_handler)
    get_by_id = staticmethod(get_child_guardian_by_id_handler)
    update = staticmethod(update_child_guardian_handler)
    delete = staticmethod(delete_child_guardian_handler)


childGuardianHandler = ChildGuardianHandler()
