from .health_facility_create_repository import create_health_facility
from .health_facility_delete_repository import delete_health_facility
from .health_facility_get_all_repository import get_all_health_facilities
from .health_facility_get_by_id_repository import get_health_facility_by_id
from .health_facility_update_repository import update_health_facility


class HealthFacilityRepository:
    create = staticmethod(create_health_facility)
    get_all = staticmethod(get_all_health_facilities)
    get_by_id = staticmethod(get_health_facility_by_id)
    update = staticmethod(update_health_facility)
    delete = staticmethod(delete_health_facility)


healthFacilityRepository = HealthFacilityRepository()
