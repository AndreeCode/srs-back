from datetime import date, datetime, timezone
from typing import Optional
from uuid import UUID

from asyncpg.exceptions import ForeignKeyViolationError
from fastapi import Request
from pydantic import BaseModel, Field

from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..domain.claim_domain import Claim, ClaimStatus
from ..domain.claim_errors import ClaimValidationError
from ..services.claims_service import claimService
from .claim_errors_handler import foreign_key_violation_error


class ClaimUpdateRequest(BaseModel):
    health_facility_id: Optional[UUID] = None
    service_id: Optional[UUID] = None
    attention_date: Optional[date] = None
    message: Optional[str] = Field(default=None, min_length=1)
    status: Optional[ClaimStatus] = None
    response: Optional[str] = None


async def update_claim_handler(request: Request, claim_id: str, body: ClaimUpdateRequest):
    try:
        claim_uuid = parse_uuid(claim_id, "claim_id")
        current = await claimService.get_by_id(claim_uuid)

        if current is None:
            return error(404, "Reclamo no encontrado", ValueError(f"claim_id={claim_id}"))

        sent = body.model_fields_set
        status = body.status if body.status is not None else current.status
        response = body.response if "response" in sent else current.response
        reviewed = status != current.status or response != current.response

        claim = Claim(
            id=current.id,
            child_id=current.child_id,
            requester_user_id=current.requester_user_id,
            requester_dni=current.requester_dni,
            child_dni=current.child_dni,
            child_identifier=current.child_identifier,
            health_facility_id=body.health_facility_id if "health_facility_id" in sent else current.health_facility_id,
            service_id=body.service_id if "service_id" in sent else current.service_id,
            attention_date=body.attention_date if "attention_date" in sent else current.attention_date,
            message=body.message if body.message is not None else current.message,
            status=status,
            response=response,
            reviewed_by=UUID(request.state.user["sub"]) if reviewed else current.reviewed_by,
            reviewed_at=datetime.now(timezone.utc) if reviewed else current.reviewed_at,
        )

        updated = await claimService.update(claim, current)

        if updated is None:
            return error(404, "Reclamo no encontrado", ValueError(f"claim_id={claim_id}"))

        return success(200, "Reclamo actualizado correctamente", updated.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except ClaimValidationError as err:
        return error(400, str(err), err)

    except ForeignKeyViolationError as err:
        return foreign_key_violation_error(err)

    except Exception as err:
        return error(500, "Error al actualizar el reclamo", err)
