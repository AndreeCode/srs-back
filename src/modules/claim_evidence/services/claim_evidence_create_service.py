from pathlib import PurePath
from uuid import UUID, uuid4

from ....core.storage.file_storage import delete_file, save_file
from ...claim.services.claims_service import claimService
from ..domain.claim_evidence_domain import MAX_EVIDENCE_BYTES, MAX_EVIDENCES_PER_CLAIM, ClaimEvidence
from ..domain.claim_evidence_errors import ClaimEvidenceValidationError
from ..repositories.claim_evidence_repositories import claimEvidenceRepository

FILE_SIGNATURES = [
    (b"\xff\xd8\xff", "image/jpeg", ".jpg"),
    (b"\x89PNG\r\n\x1a\n", "image/png", ".png"),
    (b"%PDF-", "application/pdf", ".pdf"),
]


def detect_file_type(content: bytes) -> tuple[str, str]:
    for signature, mime_type, extension in FILE_SIGNATURES:
        if content.startswith(signature):
            return mime_type, extension

    raise ClaimEvidenceValidationError("Solo se permiten archivos JPG, PNG o PDF")


async def create(claim_id: UUID, original_name: str, content: bytes) -> ClaimEvidence:
    claim = await claimService.get_by_id(claim_id)

    if claim is None:
        raise ClaimEvidenceValidationError("El claim_id indicado no existe")

    if claim.status in ("resolved", "rejected"):
        raise ClaimEvidenceValidationError("No se pueden agregar evidencias a un reclamo cerrado")

    if len(content) == 0:
        raise ClaimEvidenceValidationError("El archivo esta vacio")

    if len(content) > MAX_EVIDENCE_BYTES:
        raise ClaimEvidenceValidationError("El archivo supera los 10 MB")

    if await claimEvidenceRepository.count(claim_id) >= MAX_EVIDENCES_PER_CLAIM:
        raise ClaimEvidenceValidationError("Un reclamo puede tener como maximo 5 evidencias")

    mime_type, extension = detect_file_type(content)
    evidence_id = uuid4()
    storage_path = f"claims/{claim_id}/{evidence_id}{extension}"

    await save_file(storage_path, content)

    try:
        return await claimEvidenceRepository.create(
            ClaimEvidence(
                id=evidence_id,
                claim_id=claim_id,
                original_name=PurePath(original_name or "archivo").name[:255] or "archivo",
                storage_path=storage_path,
                mime_type=mime_type,
                size_bytes=len(content),
            )
        )
    except Exception:
        await delete_file(storage_path)
        raise
