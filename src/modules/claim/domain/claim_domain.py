from dataclasses import dataclass
from datetime import date, datetime
from typing import Literal, Optional
from uuid import UUID

ClaimStatus = Literal["pending", "in_review", "resolved", "rejected"]


@dataclass
class Claim:
    id: UUID
    child_id: UUID
    requester_user_id: UUID
    requester_dni: str
    child_identifier: str
    message: str
    child_dni: Optional[str] = None
    health_facility_id: Optional[UUID] = None
    service_id: Optional[UUID] = None
    attention_date: Optional[date] = None
    status: ClaimStatus = "pending"
    response: Optional[str] = None
    reviewed_by: Optional[UUID] = None
    reviewed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_row(cls, row) -> "Claim":
        return cls(
            id=row["id"],
            child_id=row["child_id"],
            requester_user_id=row["requester_user_id"],
            requester_dni=row["requester_dni"],
            child_identifier=row["child_identifier"],
            message=row["message"],
            child_dni=row["child_dni"],
            health_facility_id=row["health_facility_id"],
            service_id=row["service_id"],
            attention_date=row["attention_date"],
            status=row["status"],
            response=row["response"],
            reviewed_by=row["reviewed_by"],
            reviewed_at=row["reviewed_at"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "child_id": str(self.child_id),
            "requester_user_id": str(self.requester_user_id),
            "requester_dni": self.requester_dni,
            "child_dni": self.child_dni,
            "child_identifier": self.child_identifier,
            "health_facility_id": str(self.health_facility_id) if self.health_facility_id else None,
            "service_id": str(self.service_id) if self.service_id else None,
            "attention_date": self.attention_date.isoformat() if self.attention_date else None,
            "message": self.message,
            "status": self.status,
            "response": self.response,
            "reviewed_by": str(self.reviewed_by) if self.reviewed_by else None,
            "reviewed_at": self.reviewed_at.isoformat() if self.reviewed_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
