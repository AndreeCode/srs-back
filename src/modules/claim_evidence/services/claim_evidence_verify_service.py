import asyncio
import hashlib
from pathlib import Path

from ....core.logger.logger import logger
from ....core.storage.file_storage import resolve_path
from ..domain.claim_evidence_domain import ClaimEvidence
from ..domain.claim_evidence_errors import ClaimEvidenceIntegrityError
from ..repositories.claim_evidence_repositories import claimEvidenceRepository


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as source:
        while chunk := source.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


async def verified_path(evidence: ClaimEvidence) -> Path:
    path = resolve_path(evidence.storage_path)

    if not path.is_file():
        raise FileNotFoundError(str(path))

    actual = await asyncio.to_thread(file_sha256, path)

    if evidence.sha256 is None:
        await claimEvidenceRepository.set_sha256(evidence.id, actual)
        return path

    if actual != evidence.sha256:
        logger.error(f"Evidencia {evidence.id} alterada: SHA-256 esperado {evidence.sha256}, encontrado {actual}")
        raise ClaimEvidenceIntegrityError(
            "El archivo de la evidencia fue modificado en el servidor (el SHA-256 no coincide): no se entrega"
        )

    return path
