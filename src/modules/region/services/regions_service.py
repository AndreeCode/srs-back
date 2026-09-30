from .region_create_service import create
from .region_delete_service import delete
from .region_get_all_service import get_all
from .region_get_by_id_service import get_by_id
from .region_update_service import update


class RegionService:
    create = staticmethod(create)
    get_all = staticmethod(get_all)
    get_by_id = staticmethod(get_by_id)
    update = staticmethod(update)
    delete = staticmethod(delete)


regionService = RegionService()
