from fastapi import APIRouter, Depends, Request

from ...core.security.permission_guard import require_permission
from .handlers.auth_handlers import authHandler
from .handlers.auth_login_handler import LoginRequest

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(request: Request, body: LoginRequest):
    return await authHandler.login(request, body)


@router.post("/logout")
async def logout(request: Request):
    return await authHandler.logout(request)


@router.get("/me", dependencies=[Depends(require_permission("user.get:me"))])
async def me(request: Request):
    return await authHandler.me(request)
