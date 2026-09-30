from .user_region_create_handler import create_user_region_handler
from .user_region_delete_handler import delete_user_region_handler
from .user_region_get_all_handler import get_all_user_regions_handler
from .user_region_get_by_id_handler import get_user_region_by_id_handler


class UserRegionHandler:
    create = staticmethod(create_user_region_handler)
    get_all = staticmethod(get_all_user_regions_handler)
    get_by_id = staticmethod(get_user_region_by_id_handler)
    delete = staticmethod(delete_user_region_handler)


userRegionHandler = UserRegionHandler()
