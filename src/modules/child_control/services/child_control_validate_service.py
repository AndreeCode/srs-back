from datetime import date

from ...care_package.services.care_packages_service import carePackageService
from ...care_service.services.care_services_service import careServiceService
from ...child.services.children_service import childService
from ...health_facility.services.health_facilities_service import healthFacilityService
from ..domain.child_control_domain import ChildControl
from ..domain.child_control_errors import ChildControlValidationError


async def validate_child_control(child_control: ChildControl, is_new: bool, facility_changed: bool) -> None:
    if (child_control.status == "completed") != (child_control.completed_date is not None):
        raise ChildControlValidationError("Un control completed debe tener completed_date, y solo ese estado puede tenerla")

    child = await childService.get_by_id(child_control.child_id)

    if child is None:
        raise ChildControlValidationError("El child_id indicado no existe")

    if is_new and not child.active:
        raise ChildControlValidationError("El nino indicado esta inactivo")

    if child_control.completed_date is not None:
        if child_control.completed_date < child.birth_date or child_control.completed_date > date.today():
            raise ChildControlValidationError("completed_date debe estar entre la fecha de nacimiento y hoy")

    if child_control.scheduled_date is not None and child_control.scheduled_date < child.birth_date:
        raise ChildControlValidationError("scheduled_date no puede ser anterior a la fecha de nacimiento")

    if is_new:
        care_service = await careServiceService.get_by_id(child_control.service_id)

        if care_service is None:
            raise ChildControlValidationError("El service_id indicado no existe")

        if not care_service.active:
            raise ChildControlValidationError("La prestacion indicada esta inactiva")

        care_package = await carePackageService.get_by_id(care_service.package_id)

        if care_package is not None and care_package.at_risk_newborn_only and child.birth_condition == "none":
            raise ChildControlValidationError(
                "La prestacion es solo para recien nacidos en riesgo (prematuro o bajo peso)"
            )

    if facility_changed and child_control.health_facility_id is not None:
        health_facility = await healthFacilityService.get_by_id(child_control.health_facility_id)

        if health_facility is None:
            raise ChildControlValidationError("El health_facility_id indicado no existe")

        if not health_facility.active:
            raise ChildControlValidationError("El establecimiento indicado esta inactivo")
