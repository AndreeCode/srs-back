from ..domain.care_service_domain import CareService
from ..repositories.care_service_repositories import careServiceRepository
from .care_service_validate_service import validate_care_service


async def update(care_service: CareService, current: CareService) -> CareService | None:
    await validate_care_service(care_service, check_package=care_service.package_id != current.package_id)
    return await careServiceRepository.update(care_service)
