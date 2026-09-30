from .user_region_create_repository import create_user_region
from .user_region_delete_repository import delete_user_region
from .user_region_get_all_repository import get_all_user_regions
from .user_region_get_by_id_repository import get_user_region_by_id


class UserRegionRepository:
    create = staticmethod(create_user_region)
    get_all = staticmethod(get_all_user_regions)
    get_by_id = staticmethod(get_user_region_by_id)
    delete = staticmethod(delete_user_region)


userRegionRepository = UserRegionRepository()
