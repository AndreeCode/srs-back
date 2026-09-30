from uuid import UUID

from ....core.logger.logger import logger
from ....core.storage.file_storage import delete_file
from ..repositories.claim_repositories import claimRepository


async def delete(claim_id: UUID) -> str:
    storage_paths = await claimRepository.delete(claim_id)

    if storage_paths is None:
        return "not_found"

    for storage_path in storage_paths:
        try:
            await delete_file(storage_path)
        except Exception as err:
            logger.error(f"No se pudo borrar el archivo {storage_path}: {err}")

    return "deleted"
