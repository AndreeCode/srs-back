from fastapi.responses import FileResponse

from ....core.http.error import error
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..domain.claim_evidence_errors import ClaimEvidenceIntegrityError
from ..services.claim_evidences_service import claimEvidenceService


async def download_claim_evidence_handler(claim_evidence_id: str):
    try:
        claim_evidence_uuid = parse_uuid(claim_evidence_id, "claim_evidence_id")
        claim_evidence = await claimEvidenceService.get_by_id(claim_evidence_uuid)

        if claim_evidence is None:
            return error(404, "Evidencia no encontrada", ValueError(f"claim_evidence_id={claim_evidence_id}"))

        path = await claimEvidenceService.verified_path(claim_evidence)
        return FileResponse(path, media_type=claim_evidence.mime_type, filename=claim_evidence.original_name)

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except FileNotFoundError as err:
        return error(404, "El archivo de la evidencia no existe", err)

    except ClaimEvidenceIntegrityError as err:
        return error(409, str(err), err)

    except Exception as err:
        return error(500, "Error al descargar la evidencia", err)
