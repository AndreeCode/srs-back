from typing import Optional
from uuid import UUID

from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
from pydantic import BaseModel, Field

from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..domain.health_facility_domain import HealthFacility
from ..domain.health_facility_errors import HealthFacilityValidationError
from ..services.health_facilities_service import healthFacilityService


class HealthFacilityUpdateRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=250)
    region_id: Optional[UUID] = None
    active: Optional[bool] = None


async def update_health_facility_handler(health_facility_id: str, body: HealthFacilityUpdateRequest):
    try:
        health_facility_uuid = parse_uuid(health_facility_id, "health_facility_id")
        current = await healthFacilityService.get_by_id(health_facility_uuid)

        if current is None:
            return error(404, "Establecimiento no encontrado", ValueError(f"health_facility_id={health_facility_id}"))

        health_facility = HealthFacility(
            id=current.id,
            name=body.name if body.name is not None else current.name,
            region_id=body.region_id if body.region_id is not None else current.region_id,
            active=body.active if body.active is not None else current.active,
        )

        updated = await healthFacilityService.update(health_facility, current)

        if updated is None:
            return error(404, "Establecimiento no encontrado", ValueError(f"health_facility_id={health_facility_id}"))

        return success(200, "Establecimiento actualizado correctamente", updated.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except HealthFacilityValidationError as err:
        return error(400, str(err), err)

    except UniqueViolationError as err:
        return error(409, "Ya existe un establecimiento con ese nombre", err)

    except ForeignKeyViolationError as err:
        return error(400, "El region_id indicado no existe", err)

    except Exception as err:
        return error(500, "Error al actualizar el establecimiento", err)
