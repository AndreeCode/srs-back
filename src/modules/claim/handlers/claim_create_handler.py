from datetime import date
from typing import Optional
from uuid import UUID, uuid4

from asyncpg.exceptions import ForeignKeyViolationError
from fastapi import Request
from pydantic import BaseModel, Field

from ....core.http.error import error
from ....core.http.succes import success
from ..domain.claim_domain import Claim
from ..domain.claim_errors import ClaimValidationError
from ..services.claims_service import claimService
from .claim_errors_handler import foreign_key_violation_error


class ClaimCreateRequest(BaseModel):
    child_id: UUID
    requester_dni: str = Field(pattern=r"^[0-9]{8}$")
    child_dni: Optional[str] = Field(default=None, max_length=20)
    child_identifier: Optional[str] = Field(default=None, min_length=1, max_length=100)
    health_facility_id: Optional[UUID] = None
    service_id: Optional[UUID] = None
    attention_date: Optional[date] = None
    message: str = Field(min_length=1)


async def create_claim_handler(request: Request, body: ClaimCreateRequest):
    try:
        claim = Claim(
            id=uuid4(),
            child_id=body.child_id,
            requester_user_id=UUID(request.state.user["sub"]),
            requester_dni=body.requester_dni,
            child_dni=body.child_dni,
            child_identifier=body.child_identifier or "",
            health_facility_id=body.health_facility_id,
            service_id=body.service_id,
            attention_date=body.attention_date,
            message=body.message,
        )

        created = await claimService.create(claim)
        return success(201, "Reclamo registrado correctamente", created.to_dict())

    except ClaimValidationError as err:
        return error(400, str(err), err)

    except ForeignKeyViolationError as err:
        return foreign_key_violation_error(err)

    except Exception as err:
        return error(500, "Error al registrar el reclamo", err)
