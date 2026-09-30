from asyncpg.exceptions import CheckViolationError, ForeignKeyViolationError
from fastapi import UploadFile

from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..domain.claim_evidence_domain import MAX_EVIDENCE_BYTES
from ..domain.claim_evidence_errors import ClaimEvidenceValidationError
from ..services.claim_evidences_service import claimEvidenceService


async def create_claim_evidence_handler(claim_id: str, file: UploadFile):
    try:
        claim_uuid = parse_uuid(claim_id, "claim_id")
        content = await file.read(MAX_EVIDENCE_BYTES + 1)

        created = await claimEvidenceService.create(claim_uuid, file.filename or "", content)
        return success(201, "Evidencia subida correctamente", created.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except ClaimEvidenceValidationError as err:
        return error(400, str(err), err)

    except ForeignKeyViolationError as err:
        return error(400, "El claim_id indicado no existe", err)

    except CheckViolationError as err:
        return error(400, "La evidencia no cumple las reglas (tipo, tamano o maximo 5 por reclamo)", err)

    except Exception as err:
        return error(500, "Error al subir la evidencia", err)

    finally:
        await file.close()
