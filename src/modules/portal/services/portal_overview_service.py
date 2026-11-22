from uuid import UUID

from ....core.db.sqlserver import SqlServerUnavailableError
from ....core.logger.logger import logger

from ...care_package.services.care_packages_service import carePackageService
from ...care_service.services.care_services_service import careServiceService
from ...child_control.services.child_controls_service import childControlService
from ...health_facility.services.health_facilities_service import healthFacilityService
from ...guardian_his_child.services.guardian_his_children_service import guardianHisChildService
from ...his.services.his_service import hisService
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

    known_dnis = {child.dni for child, _ in children if child.dni}
    his_links = [link.to_dict() for link in await guardianHisChildService.get_all(guardian.id, None) if link.document_number not in known_dnis]
    his = {"children": [], "controls": []}
    his_error = None
    try:
        his = await hisService.followup(his_links)
    except SqlServerUnavailableError as err:
        his_error = str(err)
    except Exception as err:
        logger.error(f"No se pudo consultar HIS-MINSA: {err}")
        his_error = "No se pudo consultar a los ninos registrados en HIS-MINSA (SQL Server)"

    return {
        "guardian": guardian.to_dict(),
        "children": [{**child.to_dict(), "source": "sicna", "relationship": relationship} for child, relationship in children]
        + his["children"],
        "controls": [{**control.to_dict(), "source": "sicna"} for control in controls] + his["controls"],
        "his_error": his_error,
        "packages": [package.to_dict() for package in await carePackageService.get_all()],
        "services": [service.to_dict() for service in await careServiceService.get_all(None)],
        "facilities": [facility.to_dict() for facility in facilities],
    }
