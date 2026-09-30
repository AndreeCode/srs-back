from .care_package_create_repository import create_care_package
from .care_package_delete_repository import delete_care_package
from .care_package_get_all_repository import get_all_care_packages
from .care_package_get_by_id_repository import get_care_package_by_id
from .care_package_update_repository import update_care_package


class CarePackageRepository:
    create = staticmethod(create_care_package)
    get_all = staticmethod(get_all_care_packages)
    get_by_id = staticmethod(get_care_package_by_id)
    update = staticmethod(update_care_package)
    delete = staticmethod(delete_care_package)


carePackageRepository = CarePackageRepository()
