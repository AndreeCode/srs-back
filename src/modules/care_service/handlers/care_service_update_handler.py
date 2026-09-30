from typing import Optional
from uuid import UUID

from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
from pydantic import BaseModel, Field

from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..domain.care_service_domain import CareService
from ..domain.care_service_errors import CareServiceValidationError
from ..services.care_services_service import careServiceService


class CareServiceUpdateRequest(BaseModel):
    package_id: Optional[UUID] = None
    code: Optional[str] = Field(default=None, pattern=r"^[A-Z0-9_]{2,80}$")
    name: Optional[str] = Field(default=None, min_length=1, max_length=300)
    group_name: Optional[str] = Field(default=None, min_length=1, max_length=150)
    group_order: Optional[int] = None
    sort_order: Optional[int] = None
    min_age_days: Optional[int] = Field(default=None, ge=0)
    max_age_days: Optional[int] = Field(default=None, ge=0)
    min_interval_days: Optional[int] = Field(default=None, ge=0)
    active: Optional[bool] = None


async def update_care_service_handler(care_service_id: str, body: CareServiceUpdateRequest):
    try:
        care_service_uuid = parse_uuid(care_service_id, "care_service_id")
        current = await careServiceService.get_by_id(care_service_uuid)

        if current is None:
            return error(404, "Prestacion no encontrada", ValueError(f"care_service_id={care_service_id}"))

        care_service = CareService(
            id=current.id,
            package_id=body.package_id if body.package_id is not None else current.package_id,
            code=body.code if body.code is not None else current.code,
            name=body.name if body.name is not None else current.name,
            group_name=body.group_name if body.group_name is not None else current.group_name,
            group_order=body.group_order if body.group_order is not None else current.group_order,
            sort_order=body.sort_order if body.sort_order is not None else current.sort_order,
            min_age_days=body.min_age_days if body.min_age_days is not None else current.min_age_days,
            max_age_days=body.max_age_days if body.max_age_days is not None else current.max_age_days,
            min_interval_days=(
                body.min_interval_days if body.min_interval_days is not None else current.min_interval_days
            ),
            active=body.active if body.active is not None else current.active,
        )

        updated = await careServiceService.update(care_service, current)

        if updated is None:
            return error(404, "Prestacion no encontrada", ValueError(f"care_service_id={care_service_id}"))

        return success(200, "Prestacion actualizada correctamente", updated.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except CareServiceValidationError as err:
        return error(400, str(err), err)

    except UniqueViolationError as err:
        return error(409, "Ya existe una prestacion con ese codigo en el paquete", err)

    except ForeignKeyViolationError as err:
        return error(400, "El package_id indicado no existe", err)

    except Exception as err:
        return error(500, "Error al actualizar la prestacion", err)
