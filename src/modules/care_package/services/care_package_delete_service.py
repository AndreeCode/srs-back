from uuid import UUID

from ..repositories.care_package_repositories import carePackageRepository


async def delete(care_package_id: UUID) -> str:
    return await carePackageRepository.delete(care_package_id)
