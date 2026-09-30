from fastapi import APIRouter, Depends

from ...core.security.permission_guard import require_permission
from .handlers.session_handlers import sessionHandler

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.get("", dependencies=[Depends(require_permission("session.get"))])
async def get_all_sessions(user_id: str | None = None, device_id: str | None = None, active: bool | None = None):
    return await sessionHandler.get_all(user_id, device_id, active)


@router.get("/{session_id}", dependencies=[Depends(require_permission("session.get"))])
async def get_session_by_id(session_id: str):
    return await sessionHandler.get_by_id(session_id)


@router.delete("/{session_id}", dependencies=[Depends(require_permission("session.delete"))])
async def revoke_session(session_id: str):
    return await sessionHandler.revoke(session_id)
