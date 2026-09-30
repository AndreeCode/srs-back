from uuid import UUID

from ..domain.care_package_domain import CarePackage
from ..repositories.care_package_repositories import carePackageRepository


async def get_by_id(care_package_id: UUID) -> CarePackage | None:
    return await carePackageRepository.get_by_id(care_package_id)
