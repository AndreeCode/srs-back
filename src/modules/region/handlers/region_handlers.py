from .region_create_handler import create_region_handler
from .region_delete_handler import delete_region_handler
from .region_get_all_handler import get_all_regions_handler
from .region_get_by_id_handler import get_region_by_id_handler
from .region_update_handler import update_region_handler


class RegionHandler:
    create = staticmethod(create_region_handler)
    get_all = staticmethod(get_all_regions_handler)
    get_by_id = staticmethod(get_region_by_id_handler)
    update = staticmethod(update_region_handler)
    delete = staticmethod(delete_region_handler)


regionHandler = RegionHandler()
