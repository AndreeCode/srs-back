from .care_service_create_service import create
from .care_service_delete_service import delete
from .care_service_get_all_service import get_all
from .care_service_get_by_id_service import get_by_id
from .care_service_update_service import update


class CareServiceService:
    create = staticmethod(create)
    get_all = staticmethod(get_all)
    get_by_id = staticmethod(get_by_id)
    update = staticmethod(update)
    delete = staticmethod(delete)


careServiceService = CareServiceService()
