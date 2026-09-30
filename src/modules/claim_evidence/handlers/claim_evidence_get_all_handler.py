from ....core.http.error import error
from ....core.http.list import list_response
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.claim_evidences_service import claimEvidenceService


async def get_all_claim_evidences_handler(claim_id: str | None):
    try:
        claim_uuid = parse_uuid(claim_id, "claim_id") if claim_id is not None else None

        claim_evidences = await claimEvidenceService.get_all(claim_uuid)
        data = [claim_evidence.to_dict() for claim_evidence in claim_evidences]
        return list_response(200, "Evidencias obtenidas correctamente", data, {"count": len(data)})

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al obtener las evidencias", err)
