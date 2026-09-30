from datetime import date
from typing import Optional
from uuid import UUID, uuid4

from asyncpg.exceptions import ForeignKeyViolationError
from fastapi import Request
from pydantic import BaseModel, Field

from ....core.http.error import error
from ....core.http.succes import success
from ...claim.domain.claim_domain import Claim
from ...claim.domain.claim_errors import ClaimValidationError
from ...claim.handlers.claim_errors_handler import foreign_key_violation_error
from ..domain.portal_errors import PortalAccessError
from ..services.portal_services import portalService


class PortalClaimCreateRequest(BaseModel):
    child_id: UUID
    service_id: Optional[UUID] = None
    attention_date: Optional[date] = None
    message: str = Field(min_length=1)


async def portal_claims_handler(request: Request):
    try:
        data = await portalService.list_claims(UUID(request.state.user["sub"]))
        return success(200, "Reclamos obtenidos correctamente", data)

    except Exception as err:
        return error(500, "Error al obtener tus reclamos", err)


async def portal_claim_create_handler(request: Request, body: PortalClaimCreateRequest):
    try:
        user_id = UUID(request.state.user["sub"])
        claim = Claim(
            id=uuid4(),
            child_id=body.child_id,
            requester_user_id=user_id,
            requester_dni="",
            child_identifier="",
            service_id=body.service_id,
            attention_date=body.attention_date,
            message=body.message,
        )

        created = await portalService.create_claim(user_id, claim)
        return success(201, "Reclamo enviado correctamente", created.to_dict())

    except PortalAccessError as err:
        return error(403, str(err), err)

    except ClaimValidationError as err:
        return error(400, str(err), err)

    except ForeignKeyViolationError as err:
        return foreign_key_violation_error(err)

    except Exception as err:
        return error(500, "Error al enviar el reclamo", err)
