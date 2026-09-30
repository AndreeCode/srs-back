from .care_package_create_handler import create_care_package_handler
from .care_package_delete_handler import delete_care_package_handler
from .care_package_get_all_handler import get_all_care_packages_handler
from .care_package_get_by_id_handler import get_care_package_by_id_handler
from .care_package_update_handler import update_care_package_handler


class CarePackageHandler:
    create = staticmethod(create_care_package_handler)
    get_all = staticmethod(get_all_care_packages_handler)
    get_by_id = staticmethod(get_care_package_by_id_handler)
    update = staticmethod(update_care_package_handler)
    delete = staticmethod(delete_care_package_handler)


carePackageHandler = CarePackageHandler()
