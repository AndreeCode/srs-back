from typing import Optional

from asyncpg.exceptions import UniqueViolationError
from pydantic import BaseModel, Field

from ....core.http.error import error
from ....core.http.succes import success
from ....core.http.uuid_param import InvalidUUIDError, parse_uuid
from ..domain.care_package_domain import CarePackage
from ..domain.care_package_errors import CarePackageValidationError
from ..services.care_packages_service import carePackageService


class CarePackageUpdateRequest(BaseModel):
    code: Optional[str] = Field(default=None, pattern=r"^[A-Z0-9_]{2,50}$")
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=500)
    min_age_days: Optional[int] = Field(default=None, ge=0)
    max_age_days: Optional[int] = Field(default=None, ge=0)
    at_risk_newborn_only: Optional[bool] = None
    sort_order: Optional[int] = None
    active: Optional[bool] = None


async def update_care_package_handler(care_package_id: str, body: CarePackageUpdateRequest):
    try:
        care_package_uuid = parse_uuid(care_package_id, "care_package_id")
        current = await carePackageService.get_by_id(care_package_uuid)

        if current is None:
            return error(404, "Paquete de atencion no encontrado", ValueError(f"care_package_id={care_package_id}"))

        care_package = CarePackage(
            id=current.id,
            code=body.code if body.code is not None else current.code,
            name=body.name if body.name is not None else current.name,
            description=body.description if "description" in body.model_fields_set else current.description,
            min_age_days=body.min_age_days if body.min_age_days is not None else current.min_age_days,
            max_age_days=body.max_age_days if body.max_age_days is not None else current.max_age_days,
            at_risk_newborn_only=(
                body.at_risk_newborn_only if body.at_risk_newborn_only is not None else current.at_risk_newborn_only
            ),
            sort_order=body.sort_order if body.sort_order is not None else current.sort_order,
            active=body.active if body.active is not None else current.active,
        )

        updated = await carePackageService.update(care_package)

        if updated is None:
            return error(404, "Paquete de atencion no encontrado", ValueError(f"care_package_id={care_package_id}"))

        return success(200, "Paquete de atencion actualizado correctamente", updated.to_dict())

    except InvalidUUIDError as err:
        return error(400, str(err), err)

    except CarePackageValidationError as err:
        return error(400, str(err), err)

    except UniqueViolationError as err:
        return error(409, "Ya existe un paquete de atencion con ese codigo", err)

    except Exception as err:
        return error(500, "Error al actualizar el paquete de atencion", err)
