from typing import Optional

from ....core.http.error import error
from ....core.http.list import list_response
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..domain.claim_domain import ClaimStatus
from ..services.claims_service import claimService


async def get_all_claims_handler(
    child_id: str | None,
    requester_user_id: str | None,
    status: Optional[ClaimStatus],
):
    try:
        child_uuid = parse_uuid(child_id, "child_id") if child_id is not None else None
        requester_uuid = parse_uuid(requester_user_id, "requester_user_id") if requester_user_id is not None else None

        claims = await claimService.get_all(child_uuid, requester_uuid, status)
        data = [claim.to_dict() for claim in claims]
        return list_response(200, "Reclamos obtenidos correctamente", data, {"count": len(data)})

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al obtener los reclamos", err)
