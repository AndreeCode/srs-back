from uuid import UUID

from fastapi import APIRouter, Depends, Request

from ...core.security.permission_guard import require_permission
from .handlers.auth_handlers import authHandler
from .handlers.auth_login_handler import LoginRequest, MfaLoginRequest
from .handlers.auth_mfa_handler import MfaCodeRequest, MfaDisableRequest, PasswordConfirmRequest
from .handlers.auth_password_handler import ChangePasswordRequest
from .handlers.auth_register_handler import RegisterRequest

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(request: Request, body: LoginRequest):
    return await authHandler.login(request, body)


@router.post("/register")
async def register(request: Request, body: RegisterRequest):
    return await authHandler.register(request, body)


@router.post("/logout")
async def logout(request: Request):
    return await authHandler.logout(request)


@router.get("/me", dependencies=[Depends(require_permission("user.get:me"))])
async def me(request: Request):
    return await authHandler.me(request)


@router.put("/password", dependencies=[Depends(require_permission("user.get:me"))])
async def change_password(request: Request, body: ChangePasswordRequest):
    return await authHandler.change_password(request, body)


@router.post("/login/mfa")
async def login_mfa(request: Request, body: MfaLoginRequest):
    return await authHandler.mfa_login(request, body)


@router.get("/mfa", dependencies=[Depends(require_permission("user.get:me"))])
async def mfa_status(request: Request):
    return await authHandler.mfa_status(request)


@router.post("/mfa/setup", dependencies=[Depends(require_permission("user.get:me"))])
async def mfa_setup(request: Request, body: PasswordConfirmRequest):
    return await authHandler.mfa_setup(request, body)


@router.post("/mfa/enable", dependencies=[Depends(require_permission("user.get:me"))])
async def mfa_enable(request: Request, body: MfaCodeRequest):
    return await authHandler.mfa_enable(request, body)


@router.post("/mfa/disable", dependencies=[Depends(require_permission("user.get:me"))])
async def mfa_disable(request: Request, body: MfaDisableRequest):
    return await authHandler.mfa_disable(request, body)


@router.get("/sessions", dependencies=[Depends(require_permission("user.get:me"))])
async def my_sessions(request: Request):
    return await authHandler.my_sessions(request)


@router.post("/sessions/revoke-others", dependencies=[Depends(require_permission("user.get:me"))])
async def revoke_my_other_sessions(request: Request, body: PasswordConfirmRequest):
    return await authHandler.revoke_my_other_sessions(request, body)


@router.post("/sessions/{session_id}/revoke", dependencies=[Depends(require_permission("user.get:me"))])
async def revoke_my_session(request: Request, session_id: UUID, body: PasswordConfirmRequest):
    return await authHandler.revoke_my_session(request, session_id, body)
