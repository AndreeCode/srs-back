from typing import Optional
from uuid import uuid4

from asyncpg.exceptions import UniqueViolationError
from pydantic import BaseModel, Field

from ....core.http.error import error
from ....core.http.succes import success
from ..domain.care_package_domain import CarePackage
from ..domain.care_package_errors import CarePackageValidationError
from ..services.care_packages_service import carePackageService


class CarePackageCreateRequest(BaseModel):
    code: str = Field(pattern=r"^[A-Z0-9_]{2,50}$")
    name: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=500)
    min_age_days: int = Field(ge=0)
    max_age_days: int = Field(ge=0)
    at_risk_newborn_only: bool = False
    sort_order: int = 1


async def create_care_package_handler(body: CarePackageCreateRequest):
    try:
        care_package = CarePackage(
            id=uuid4(),
            code=body.code,
            name=body.name,
            description=body.description,
            min_age_days=body.min_age_days,
            max_age_days=body.max_age_days,
            at_risk_newborn_only=body.at_risk_newborn_only,
            sort_order=body.sort_order,
        )

        created = await carePackageService.create(care_package)
        return success(201, "Paquete de atencion creado correctamente", created.to_dict())

    except CarePackageValidationError as err:
        return error(400, str(err), err)

    except UniqueViolationError as err:
        return error(409, "Ya existe un paquete de atencion con ese codigo", err)

    except Exception as err:
        return error(500, "Error al crear el paquete de atencion", err)
