from uuid import UUID

from ....core.logger.logger import logger
from ....core.storage.file_storage import delete_file
from ..repositories.claim_evidence_repositories import claimEvidenceRepository


async def delete(claim_evidence_id: UUID) -> str:
    storage_path = await claimEvidenceRepository.delete(claim_evidence_id)

    if storage_path is None:
        return "not_found"

    try:
        await delete_file(storage_path)
    except Exception as err:
        logger.error(f"No se pudo borrar el archivo {storage_path}: {err}")

    return "deleted"
