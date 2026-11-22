from .guardian_create_repository import create_guardian
from .guardian_delete_repository import delete_guardian
from .guardian_discard_repository import discard_new_guardian
from .guardian_get_all_repository import get_all_guardians
from .guardian_link_attempt_repository import count_link_failures, record_link_attempt
from .guardian_pending_link_repository import approve_pending_link, get_pending_links, reject_pending_link
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
    discard_new = staticmethod(discard_new_guardian)
    count_link_failures = staticmethod(count_link_failures)
    record_link_attempt = staticmethod(record_link_attempt)
    get_pending_links = staticmethod(get_pending_links)
    approve_pending_link = staticmethod(approve_pending_link)
    reject_pending_link = staticmethod(reject_pending_link)


guardianRepository = GuardianRepository()
