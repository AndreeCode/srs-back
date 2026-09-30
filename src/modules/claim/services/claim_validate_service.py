from datetime import date

from ...care_service.services.care_services_service import careServiceService
from ...health_facility.services.health_facilities_service import healthFacilityService
from ..domain.claim_domain import Claim
from ..domain.claim_errors import ClaimValidationError


async def validate_claim(claim: Claim, current: Claim | None) -> None:
    if claim.attention_date is not None and claim.attention_date > date.today():
        raise ClaimValidationError("attention_date no puede ser futura")

    if claim.status in ("resolved", "rejected") and not claim.response:
        raise ClaimValidationError("Para resolver o rechazar un reclamo debe enviar response")

    if claim.service_id is not None and (current is None or claim.service_id != current.service_id):
        if await careServiceService.get_by_id(claim.service_id) is None:
            raise ClaimValidationError("El service_id indicado no existe")

    if claim.health_facility_id is not None and (
        current is None or claim.health_facility_id != current.health_facility_id
    ):
        if await healthFacilityService.get_by_id(claim.health_facility_id) is None:
            raise ClaimValidationError("El health_facility_id indicado no existe")
