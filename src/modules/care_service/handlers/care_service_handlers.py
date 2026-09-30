from .care_service_create_handler import create_care_service_handler
from .care_service_delete_handler import delete_care_service_handler
from .care_service_get_all_handler import get_all_care_services_handler
from .care_service_get_by_id_handler import get_care_service_by_id_handler
from .care_service_update_handler import update_care_service_handler


class CareServiceHandler:
    create = staticmethod(create_care_service_handler)
    get_all = staticmethod(get_all_care_services_handler)
    get_by_id = staticmethod(get_care_service_by_id_handler)
    update = staticmethod(update_care_service_handler)
    delete = staticmethod(delete_care_service_handler)


careServiceHandler = CareServiceHandler()
