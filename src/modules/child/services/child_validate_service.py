from datetime import date
from uuid import UUID

from ...health_facility.services.health_facilities_service import healthFacilityService
from ..domain.child_domain import Child
from ..domain.child_errors import ChildValidationError


def validate_child(child: Child) -> None:
    if child.birth_date > date.today():
        raise ChildValidationError("La fecha de nacimiento no puede ser futura")


async def validate_health_facility(health_facility_id: UUID) -> None:
    health_facility = await healthFacilityService.get_by_id(health_facility_id)

    if health_facility is None:
        raise ChildValidationError("El health_facility_id indicado no existe")

    if not health_facility.active:
        raise ChildValidationError("El establecimiento indicado esta inactivo")
