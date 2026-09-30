from uuid import UUID

from ...care_package.services.care_packages_service import carePackageService
from ...care_service.services.care_services_service import careServiceService
from ...child_control.services.child_controls_service import childControlService
from ...health_facility.services.health_facilities_service import healthFacilityService
from ..repositories.portal_repositories import portalRepository
from .portal_access_service import get_guardian


async def overview(user_id: UUID) -> dict:
    guardian = await get_guardian(user_id)
    children = await portalRepository.get_children_of_guardian(guardian.id)

    controls = []
    for child, _ in children:
        controls += await childControlService.get_all(child.id, None, None)

    facility_ids = {child.health_facility_id for child, _ in children} | {
        control.health_facility_id for control in controls if control.health_facility_id
    }
    facilities = [f for f in await healthFacilityService.get_all(None) if f.id in facility_ids]

    return {
        "guardian": guardian.to_dict(),
        "children": [{**child.to_dict(), "relationship": relationship} for child, relationship in children],
        "controls": [control.to_dict() for control in controls],
        "packages": [package.to_dict() for package in await carePackageService.get_all()],
        "services": [service.to_dict() for service in await careServiceService.get_all(None)],
        "facilities": [facility.to_dict() for facility in facilities],
    }
