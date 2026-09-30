from uuid import UUID

from fastapi import HTTPException, Request

from ...modules.permission.domain.permission_catalog import PERMISSIONS
from ...modules.permission.services.permissions_service import permissionService


def require_permission(code: str):
    if code not in PERMISSIONS:
        raise ValueError(f"Permiso desconocido '{code}': agregalo a permission_catalog.PERMISSIONS")

    async def dependency(request: Request) -> None:
        user = getattr(request.state, "user", None)

        if user is None:
            raise HTTPException(status_code=401, detail="No autenticado")

        if not await permissionService.user_has(UUID(user["sub"]), code):
            raise HTTPException(status_code=403, detail=f"No tienes permiso para esta accion ({code})")

    return dependency
