from uuid import UUID, uuid4

from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
from pydantic import BaseModel, Field

from ....core.http.error import error
from ....core.http.succes import success
from ..domain.health_facility_domain import HealthFacility
from ..domain.health_facility_errors import HealthFacilityValidationError
from ..services.health_facilities_service import healthFacilityService


class HealthFacilityCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=250)
    region_id: UUID


async def create_health_facility_handler(body: HealthFacilityCreateRequest):
    try:
        health_facility = HealthFacility(id=uuid4(), name=body.name, region_id=body.region_id)
        created = await healthFacilityService.create(health_facility)
        return success(201, "Establecimiento creado correctamente", created.to_dict())

    except HealthFacilityValidationError as err:
        return error(400, str(err), err)

    except UniqueViolationError as err:
        return error(409, "Ya existe un establecimiento con ese nombre", err)

    except ForeignKeyViolationError as err:
        return error(400, "El region_id indicado no existe", err)

    except Exception as err:
        return error(500, "Error al crear el establecimiento", err)
