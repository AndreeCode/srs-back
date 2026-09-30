from dataclasses import dataclass
from datetime import date, datetime
from typing import Literal, Optional
from uuid import UUID

ControlStatus = Literal["pending", "completed", "overdue", "not_applicable"]


@dataclass
class ChildControl:
    id: UUID
    child_id: UUID
    service_id: UUID
    status: ControlStatus = "pending"
    scheduled_date: Optional[date] = None
    completed_date: Optional[date] = None
    health_facility_id: Optional[UUID] = None
    batch_number: Optional[str] = None
    book_page: Optional[str] = None
    book_record: Optional[str] = None
    notes: Optional[str] = None
    registered_by: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_row(cls, row) -> "ChildControl":
        return cls(
            id=row["id"],
            child_id=row["child_id"],
            service_id=row["service_id"],
            status=row["status"],
            scheduled_date=row["scheduled_date"],
            completed_date=row["completed_date"],
            health_facility_id=row["health_facility_id"],
            batch_number=row["batch_number"],
            book_page=row["book_page"],
            book_record=row["book_record"],
            notes=row["notes"],
            registered_by=row["registered_by"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "child_id": str(self.child_id),
            "service_id": str(self.service_id),
            "status": self.status,
            "scheduled_date": self.scheduled_date.isoformat() if self.scheduled_date else None,
            "completed_date": self.completed_date.isoformat() if self.completed_date else None,
            "health_facility_id": str(self.health_facility_id) if self.health_facility_id else None,
            "batch_number": self.batch_number,
            "book_page": self.book_page,
            "book_record": self.book_record,
            "notes": self.notes,
            "registered_by": str(self.registered_by) if self.registered_by else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
