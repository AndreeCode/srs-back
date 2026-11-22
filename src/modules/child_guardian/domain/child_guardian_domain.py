from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class ChildGuardian:
    child_id: UUID
    guardian_id: UUID
    relationship: Optional[str] = None
    verified: bool = True
    requested_at: Optional[datetime] = None
    verified_by: Optional[UUID] = None
    verified_at: Optional[datetime] = None

    @classmethod
    def from_row(cls, row) -> "ChildGuardian":
        return cls(
            child_id=row["child_id"],
            guardian_id=row["guardian_id"],
            relationship=row["relationship"],
            verified=row["verified"],
            requested_at=row["requested_at"],
            verified_by=row["verified_by"],
            verified_at=row["verified_at"],
        )

    def to_dict(self) -> dict:
        return {
            "child_id": str(self.child_id),
            "guardian_id": str(self.guardian_id),
            "relationship": self.relationship,
            "verified": self.verified,
            "requested_at": self.requested_at.isoformat() if self.requested_at else None,
            "verified_by": str(self.verified_by) if self.verified_by else None,
            "verified_at": self.verified_at.isoformat() if self.verified_at else None,
        }
