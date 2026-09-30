from .health_facility_create_handler import create_health_facility_handler
from .health_facility_delete_handler import delete_health_facility_handler
from .health_facility_get_all_handler import get_all_health_facilities_handler
from .health_facility_get_by_id_handler import get_health_facility_by_id_handler
from .health_facility_update_handler import update_health_facility_handler


class HealthFacilityHandler:
    create = staticmethod(create_health_facility_handler)
    get_all = staticmethod(get_all_health_facilities_handler)
    get_by_id = staticmethod(get_health_facility_by_id_handler)
    update = staticmethod(update_health_facility_handler)
    delete = staticmethod(delete_health_facility_handler)


healthFacilityHandler = HealthFacilityHandler()
