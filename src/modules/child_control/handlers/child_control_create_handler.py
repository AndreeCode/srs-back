from datetime import date
from typing import Optional
from uuid import UUID, uuid4

from asyncpg.exceptions import CheckViolationError, ForeignKeyViolationError, UniqueViolationError
from fastapi import Request
from pydantic import BaseModel, Field

from ....core.http.error import error
from ....core.http.succes import success
from ..domain.child_control_domain import ChildControl, ControlStatus
from ..domain.child_control_errors import ChildControlValidationError
from ..services.child_controls_service import childControlService
from .child_control_errors_handler import check_violation_error, foreign_key_violation_error


class ChildControlCreateRequest(BaseModel):
    child_id: UUID
    service_id: UUID
    status: Optional[ControlStatus] = None
    scheduled_date: Optional[date] = None
    completed_date: Optional[date] = None
    health_facility_id: Optional[UUID] = None
    batch_number: Optional[str] = Field(default=None, max_length=100)
    book_page: Optional[str] = Field(default=None, max_length=100)
    book_record: Optional[str] = Field(default=None, max_length=100)
    notes: Optional[str] = None


async def create_child_control_handler(request: Request, body: ChildControlCreateRequest):
    try:
        child_control = ChildControl(
            id=uuid4(),
            child_id=body.child_id,
            service_id=body.service_id,
            status=body.status or ("completed" if body.completed_date else "pending"),
            scheduled_date=body.scheduled_date,
            completed_date=body.completed_date,
            health_facility_id=body.health_facility_id,
            batch_number=body.batch_number,
            book_page=body.book_page,
            book_record=body.book_record,
            notes=body.notes,
            registered_by=UUID(request.state.user["sub"]),
        )

        created = await childControlService.create(child_control)
        return success(201, "Control registrado correctamente", created.to_dict())

    except ChildControlValidationError as err:
        return error(400, str(err), err)

    except UniqueViolationError as err:
        return error(409, "El nino ya tiene un control para esa prestacion", err)

    except ForeignKeyViolationError as err:
        return foreign_key_violation_error(err)

    except CheckViolationError as err:
        return check_violation_error(err)

    except Exception as err:
        return error(500, "Error al registrar el control", err)
