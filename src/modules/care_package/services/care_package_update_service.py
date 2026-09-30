from ..domain.care_package_domain import CarePackage
from ..repositories.care_package_repositories import carePackageRepository
from .care_package_validate_service import validate_care_package


async def update(care_package: CarePackage) -> CarePackage | None:
    validate_care_package(care_package)
    return await carePackageRepository.update(care_package)
