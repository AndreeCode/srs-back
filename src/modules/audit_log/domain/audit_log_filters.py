from dataclasses import dataclass
from datetime import date
from typing import Optional
from uuid import UUID


@dataclass
class AuditLogFilters:
    user_id: Optional[UUID] = None
    affected_table: Optional[str] = None
    record_id: Optional[UUID] = None
    action: Optional[str] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    limit: int = 100
    offset: int = 0
