from datetime import date
from typing import Literal
from uuid import UUID

from fastapi import Request
from pydantic import BaseModel, Field

from ....core.config.config import config
from ....core.db.sqlserver import SqlServerUnavailableError
from ....core.http.error import error
from ....core.http.succes import success
from ...guardian.domain.guardian_errors import GuardianChildNotFoundError, GuardianConflictError
from ..domain.portal_errors import PortalAccessError
from ..services.portal_services import portalService


class PortalLinkChildRequest(BaseModel):
    child_identifier: str = Field(min_length=3, max_length=50)
    child_birth_date: date
    relationship: Literal["Madre", "Padre", "Apoderado"] = "Madre"


async def portal_link_child_handler(request: Request, body: PortalLinkChildRequest):
    if not config.public_registration:
        return error(403, "Por ahora tus hijos los vincula tu establecimiento de salud (admin o coordinador)", PermissionError("PUBLIC_REGISTRATION=false"))

    try:
        data = await portalService.link_child(
            UUID(request.state.user["sub"]), body.child_identifier, body.child_birth_date, body.relationship
        )
        return success(201, f"{data['full_name']} fue vinculado a tu cuenta", data)

    except PortalAccessError as err:
        return error(403, str(err), err)

    except GuardianConflictError as err:
        return error(409, str(err), err)

    except GuardianChildNotFoundError as err:
        return error(404, str(err), err)

    except SqlServerUnavailableError as err:
        return error(503, f"{err}. Intenta mas tarde", err)

    except Exception as err:
        return error(500, "Error al vincular al nino", err)
