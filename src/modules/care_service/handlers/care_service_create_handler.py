from uuid import UUID, uuid4

from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
from pydantic import BaseModel, Field

from ....core.http.error import error
from ....core.http.succes import success
from ..domain.care_service_domain import CareService
from ..domain.care_service_errors import CareServiceValidationError
from ..services.care_services_service import careServiceService


class CareServiceCreateRequest(BaseModel):
    package_id: UUID
    code: str = Field(pattern=r"^[A-Z0-9_]{2,80}$")
    name: str = Field(min_length=1, max_length=300)
    group_name: str = Field(default="DIRECT", min_length=1, max_length=150)
    group_order: int = 1
    sort_order: int = 1
    min_age_days: int = Field(ge=0)
    max_age_days: int = Field(ge=0)
    min_interval_days: int = Field(default=0, ge=0)


async def create_care_service_handler(body: CareServiceCreateRequest):
    try:
        care_service = CareService(
            id=uuid4(),
            package_id=body.package_id,
            code=body.code,
            name=body.name,
            group_name=body.group_name,
            group_order=body.group_order,
            sort_order=body.sort_order,
            min_age_days=body.min_age_days,
            max_age_days=body.max_age_days,
            min_interval_days=body.min_interval_days,
        )

        created = await careServiceService.create(care_service)
        return success(201, "Prestacion creada correctamente", created.to_dict())

    except CareServiceValidationError as err:
        return error(400, str(err), err)

    except UniqueViolationError as err:
        return error(409, "Ya existe una prestacion con ese codigo en el paquete", err)

    except ForeignKeyViolationError as err:
        return error(400, "El package_id indicado no existe", err)

    except Exception as err:
        return error(500, "Error al crear la prestacion", err)
