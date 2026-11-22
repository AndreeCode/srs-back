from uuid import UUID

from asyncpg.exceptions import CheckViolationError
from fastapi import Request, UploadFile
from fastapi.responses import FileResponse

from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ...claim_evidence.domain.claim_evidence_domain import MAX_EVIDENCE_BYTES
from ...claim_evidence.domain.claim_evidence_errors import ClaimEvidenceIntegrityError, ClaimEvidenceValidationError
from ...claim_evidence.services.claim_evidences_service import claimEvidenceService
from ..domain.portal_errors import PortalNotFoundError
from ..services.portal_services import portalService


async def portal_evidence_create_handler(request: Request, claim_id: str, file: UploadFile):
    try:
        claim_uuid = parse_uuid(claim_id, "claim_id")
        content = await file.read(MAX_EVIDENCE_BYTES + 1)

        created = await portalService.upload_evidence(
            UUID(request.state.user["sub"]), claim_uuid, file.filename or "", content
        )
        return success(201, "Evidencia adjuntada correctamente", created.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except PortalNotFoundError as err:
        return error(404, str(err), err)

    except ClaimEvidenceValidationError as err:
        return error(400, str(err), err)

    except CheckViolationError as err:
        return error(400, "La evidencia no cumple las reglas (tipo, tamano o maximo 5 por reclamo)", err)

    except Exception as err:
        return error(500, "Error al adjuntar la evidencia", err)

    finally:
        await file.close()


async def portal_evidence_download_handler(request: Request, claim_evidence_id: str):
    try:
        evidence = await portalService.get_evidence(
            UUID(request.state.user["sub"]), parse_uuid(claim_evidence_id, "claim_evidence_id")
        )
        path = await claimEvidenceService.verified_path(evidence)
        return FileResponse(path, media_type=evidence.mime_type, filename=evidence.original_name)

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except FileNotFoundError as err:
        return error(404, "El archivo de la evidencia no existe", err)

    except ClaimEvidenceIntegrityError as err:
        return error(409, str(err), err)

    except PortalNotFoundError as err:
        return error(404, str(err), err)

    except Exception as err:
        return error(500, "Error al descargar la evidencia", err)
