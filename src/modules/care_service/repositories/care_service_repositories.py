from .care_service_create_repository import create_care_service
from .care_service_delete_repository import delete_care_service
from .care_service_get_all_repository import get_all_care_services
from .care_service_get_by_id_repository import get_care_service_by_id
from .care_service_update_repository import update_care_service


class CareServiceRepository:
    create = staticmethod(create_care_service)
    get_all = staticmethod(get_all_care_services)
    get_by_id = staticmethod(get_care_service_by_id)
    update = staticmethod(update_care_service)
    delete = staticmethod(delete_care_service)


careServiceRepository = CareServiceRepository()
