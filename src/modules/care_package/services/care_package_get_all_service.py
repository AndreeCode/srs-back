from ..domain.care_package_domain import CarePackage
from ..repositories.care_package_repositories import carePackageRepository


async def get_all() -> list[CarePackage]:
    return await carePackageRepository.get_all()
