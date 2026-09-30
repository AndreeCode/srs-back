from datetime import date
from typing import Optional
from uuid import UUID

from asyncpg.exceptions import CheckViolationError, ForeignKeyViolationError
from pydantic import BaseModel, Field

from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..domain.child_control_domain import ChildControl, ControlStatus
from ..domain.child_control_errors import ChildControlValidationError
from ..services.child_controls_service import childControlService
from .child_control_errors_handler import check_violation_error, foreign_key_violation_error


class ChildControlUpdateRequest(BaseModel):
    status: Optional[ControlStatus] = None
    scheduled_date: Optional[date] = None
    completed_date: Optional[date] = None
    health_facility_id: Optional[UUID] = None
    batch_number: Optional[str] = Field(default=None, max_length=100)
    book_page: Optional[str] = Field(default=None, max_length=100)
    book_record: Optional[str] = Field(default=None, max_length=100)
    notes: Optional[str] = None


async def update_child_control_handler(child_control_id: str, body: ChildControlUpdateRequest):
    try:
        child_control_uuid = parse_uuid(child_control_id, "child_control_id")
        current = await childControlService.get_by_id(child_control_uuid)

        if current is None:
            return error(404, "Control no encontrado", ValueError(f"child_control_id={child_control_id}"))

        sent = body.model_fields_set
        completed_date = body.completed_date if "completed_date" in sent else current.completed_date

        if body.status is not None:
            status = body.status
        elif completed_date is not None:
            status = "completed"
        elif current.status == "completed":
            status = "pending"
        else:
            status = current.status

        child_control = ChildControl(
            id=current.id,
            child_id=current.child_id,
            service_id=current.service_id,
            status=status,
            scheduled_date=body.scheduled_date if "scheduled_date" in sent else current.scheduled_date,
            completed_date=completed_date,
            health_facility_id=body.health_facility_id if "health_facility_id" in sent else current.health_facility_id,
            batch_number=body.batch_number if "batch_number" in sent else current.batch_number,
            book_page=body.book_page if "book_page" in sent else current.book_page,
            book_record=body.book_record if "book_record" in sent else current.book_record,
            notes=body.notes if "notes" in sent else current.notes,
            registered_by=current.registered_by,
        )

        updated = await childControlService.update(child_control, current)

        if updated is None:
            return error(404, "Control no encontrado", ValueError(f"child_control_id={child_control_id}"))

        return success(200, "Control actualizado correctamente", updated.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except ChildControlValidationError as err:
        return error(400, str(err), err)

    except ForeignKeyViolationError as err:
        return foreign_key_violation_error(err)

    except CheckViolationError as err:
        return check_violation_error(err)

    except Exception as err:
        return error(500, "Error al actualizar el control", err)
