from ...care_package.services.care_packages_service import carePackageService
from ..domain.care_service_domain import CareService
from ..domain.care_service_errors import CareServiceValidationError


async def validate_care_service(care_service: CareService, check_package: bool) -> None:
    if care_service.min_age_days > care_service.max_age_days:
        raise CareServiceValidationError("min_age_days no puede ser mayor que max_age_days")

    if not check_package:
        return

    care_package = await carePackageService.get_by_id(care_service.package_id)

    if care_package is None:
        raise CareServiceValidationError("El package_id indicado no existe")

    if not care_package.active:
        raise CareServiceValidationError("El paquete de atencion indicado esta inactivo")
