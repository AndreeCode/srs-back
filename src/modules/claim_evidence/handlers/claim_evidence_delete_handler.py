from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.claim_evidences_service import claimEvidenceService


async def delete_claim_evidence_handler(claim_evidence_id: str):
    try:
        claim_evidence_uuid = parse_uuid(claim_evidence_id, "claim_evidence_id")
        result = await claimEvidenceService.delete(claim_evidence_uuid)

        if result == "not_found":
            return error(404, "Evidencia no encontrada", ValueError(f"claim_evidence_id={claim_evidence_id}"))

        return success(200, "Evidencia eliminada correctamente")

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al eliminar la evidencia", err)
