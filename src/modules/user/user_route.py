from uuid import UUID

from fastapi import APIRouter, Depends, Request

from ...core.security.permission_guard import require_permission
from .handlers.user_create_handler import UserCreateRequest
from .handlers.user_handlers import userHandler
from .handlers.user_update_handler import UserUpdateRequest

router = APIRouter(prefix="/users", tags=["users"])


def caller(request: Request) -> UUID:
    return UUID(request.state.user["sub"])


@router.post("", dependencies=[Depends(require_permission("user.post"))])
async def create_user(request: Request, body: UserCreateRequest):
    return await userHandler.create(caller(request), body)


@router.get("", dependencies=[Depends(require_permission("user.get"))])
async def get_all_users():
    return await userHandler.get_all()


@router.get("/{user_id}", dependencies=[Depends(require_permission("user.get"))])
async def get_user_by_id(user_id: str):
    return await userHandler.get_by_id(user_id)


@router.put("/{user_id}", dependencies=[Depends(require_permission("user.put"))])
async def update_user(request: Request, user_id: str, body: UserUpdateRequest):
    return await userHandler.update(caller(request), user_id, body)


@router.delete("/{user_id}", dependencies=[Depends(require_permission("user.delete"))])
async def delete_user(request: Request, user_id: str):
    return await userHandler.delete(caller(request), user_id)
