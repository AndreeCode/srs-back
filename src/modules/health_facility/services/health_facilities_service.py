from .health_facility_create_service import create
from .health_facility_delete_service import delete
from .health_facility_get_all_service import get_all
from .health_facility_get_by_id_service import get_by_id
from .health_facility_update_service import update


class HealthFacilityService:
    create = staticmethod(create)
    get_all = staticmethod(get_all)
    get_by_id = staticmethod(get_by_id)
    update = staticmethod(update)
    delete = staticmethod(delete)


healthFacilityService = HealthFacilityService()
