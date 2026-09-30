from ..domain.care_service_domain import CareService
from ..repositories.care_service_repositories import careServiceRepository
from .care_service_validate_service import validate_care_service


async def create(care_service: CareService) -> CareService:
    await validate_care_service(care_service, check_package=True)
    return await careServiceRepository.create(care_service)
