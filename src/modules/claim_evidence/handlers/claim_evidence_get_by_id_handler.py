from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..services.claim_evidences_service import claimEvidenceService


async def get_claim_evidence_by_id_handler(claim_evidence_id: str):
    try:
        claim_evidence_uuid = parse_uuid(claim_evidence_id, "claim_evidence_id")
        claim_evidence = await claimEvidenceService.get_by_id(claim_evidence_uuid)

        if claim_evidence is None:
            return error(404, "Evidencia no encontrada", ValueError(f"claim_evidence_id={claim_evidence_id}"))

        return success(200, "Evidencia obtenida correctamente", claim_evidence.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except Exception as err:
        return error(500, "Error al obtener la evidencia", err)
