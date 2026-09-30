from ..domain.care_package_domain import CarePackage
from ..repositories.care_package_repositories import carePackageRepository
from .care_package_validate_service import validate_care_package


async def create(care_package: CarePackage) -> CarePackage:
    validate_care_package(care_package)
    return await carePackageRepository.create(care_package)
