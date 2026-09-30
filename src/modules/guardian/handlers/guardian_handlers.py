from .guardian_create_handler import create_guardian_handler
from .guardian_delete_handler import delete_guardian_handler
from .guardian_get_all_handler import get_all_guardians_handler
from .guardian_get_by_id_handler import get_guardian_by_id_handler
from .guardian_update_handler import update_guardian_handler


class GuardianHandler:
    create = staticmethod(create_guardian_handler)
    get_all = staticmethod(get_all_guardians_handler)
    get_by_id = staticmethod(get_guardian_by_id_handler)
    update = staticmethod(update_guardian_handler)
    delete = staticmethod(delete_guardian_handler)


guardianHandler = GuardianHandler()
