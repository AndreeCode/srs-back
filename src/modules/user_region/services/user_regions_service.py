from .user_region_create_service import create
from .user_region_delete_service import delete
from .user_region_get_all_service import get_all
from .user_region_get_by_id_service import get_by_id


class UserRegionService:
    create = staticmethod(create)
    get_all = staticmethod(get_all)
    get_by_id = staticmethod(get_by_id)
    delete = staticmethod(delete)


userRegionService = UserRegionService()
