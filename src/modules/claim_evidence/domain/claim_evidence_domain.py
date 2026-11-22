from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

MAX_EVIDENCE_BYTES = 10 * 1024 * 1024
MAX_EVIDENCES_PER_CLAIM = 5


@dataclass
class ClaimEvidence:
    id: UUID
    claim_id: UUID
    original_name: str
    storage_path: str
    mime_type: str
    size_bytes: int
    created_at: Optional[datetime] = None
    sha256: Optional[str] = None

    @classmethod
    def from_row(cls, row) -> "ClaimEvidence":
        return cls(
            id=row["id"],
            claim_id=row["claim_id"],
            original_name=row["original_name"],
            storage_path=row["storage_path"],
            mime_type=row["mime_type"],
            size_bytes=row["size_bytes"],
            created_at=row["created_at"],
            sha256=row["sha256"].strip() if row["sha256"] else None,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "claim_id": str(self.claim_id),
            "original_name": self.original_name,
            "mime_type": self.mime_type,
            "size_bytes": self.size_bytes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "sha256": self.sha256,
        }
