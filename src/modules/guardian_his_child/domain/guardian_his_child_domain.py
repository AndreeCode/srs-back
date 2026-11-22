from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional
from uuid import UUID


@dataclass
class GuardianHisChild:
    guardian_id: UUID
    document_number: str
    birth_date: date
    relationship: str = "Guardian"
    child_name: Optional[str] = None
    linked_by: Optional[UUID] = None
    created_at: Optional[datetime] = None
    verified: bool = True
    verified_by: Optional[UUID] = None
    verified_at: Optional[datetime] = None

    @classmethod
    def from_row(cls, row) -> "GuardianHisChild":
        return cls(
            guardian_id=row["guardian_id"],
            document_number=row["document_number"],
            birth_date=row["birth_date"],
            relationship=row["relationship"],
            child_name=row["child_name"],
            linked_by=row["linked_by"],
            created_at=row["created_at"],
            verified=row["verified"],
            verified_by=row["verified_by"],
            verified_at=row["verified_at"],
        )

    def to_dict(self) -> dict:
        return {
            "guardian_id": str(self.guardian_id),
            "document_number": self.document_number,
            "birth_date": self.birth_date.isoformat(),
            "relationship": self.relationship,
            "child_name": self.child_name,
            "linked_by": str(self.linked_by) if self.linked_by else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "verified": self.verified,
            "verified_by": str(self.verified_by) if self.verified_by else None,
            "verified_at": self.verified_at.isoformat() if self.verified_at else None,
        }
