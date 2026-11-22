from .guardian_create_repository import create_guardian
from .guardian_delete_repository import delete_guardian
from .guardian_get_all_repository import get_all_guardians
from .guardian_get_by_dni_repository import get_guardian_by_dni
from .guardian_get_by_id_repository import get_guardian_by_id
from .guardian_update_repository import update_guardian


class GuardianRepository:
    create = staticmethod(create_guardian)
    get_all = staticmethod(get_all_guardians)
    get_by_id = staticmethod(get_guardian_by_id)
    get_by_dni = staticmethod(get_guardian_by_dni)
    update = staticmethod(update_guardian)
    delete = staticmethod(delete_guardian)


guardianRepository = GuardianRepository()
