from typing import Optional
from uuid import uuid4

from asyncpg.exceptions import UniqueViolationError
from pydantic import BaseModel, Field

from ....core.http.error import error
from ....core.http.succes import success
from ..domain.region_domain import Region
from ..services.regions_service import regionService


class RegionCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    health_network: Optional[str] = Field(default=None, min_length=1, max_length=150)


async def create_region_handler(body: RegionCreateRequest):
    try:
        region = Region(id=uuid4(), name=body.name, health_network=body.health_network)
        created = await regionService.create(region)
        return success(201, "Micro red creada correctamente", created.to_dict())

    except UniqueViolationError as err:
        return error(409, "Ya existe una micro red con ese nombre", err)

    except Exception as err:
        return error(500, "Error al crear la micro red", err)
