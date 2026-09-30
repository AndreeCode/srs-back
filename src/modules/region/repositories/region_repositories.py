from .region_create_repository import create_region
from .region_delete_repository import delete_region
from .region_get_all_repository import get_all_regions
from .region_get_by_id_repository import get_region_by_id
from .region_update_repository import update_region


class RegionRepository:
    create = staticmethod(create_region)
    get_all = staticmethod(get_all_regions)
    get_by_id = staticmethod(get_region_by_id)
    update = staticmethod(update_region)
    delete = staticmethod(delete_region)


regionRepository = RegionRepository()
