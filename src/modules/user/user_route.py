from fastapi import APIRouter, Depends

from ...core.security.permission_guard import require_permission
from .handlers.user_create_handler import UserCreateRequest
from .handlers.user_handlers import userHandler
from .handlers.user_update_handler import UserUpdateRequest

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", dependencies=[Depends(require_permission("user.post"))])
async def create_user(body: UserCreateRequest):
    return await userHandler.create(body)


@router.get("", dependencies=[Depends(require_permission("user.get"))])
async def get_all_users():
    return await userHandler.get_all()


@router.get("/{user_id}", dependencies=[Depends(require_permission("user.get"))])
async def get_user_by_id(user_id: str):
    return await userHandler.get_by_id(user_id)


@router.put("/{user_id}", dependencies=[Depends(require_permission("user.put"))])
async def update_user(user_id: str, body: UserUpdateRequest):
    return await userHandler.update(user_id, body)


@router.delete("/{user_id}", dependencies=[Depends(require_permission("user.delete"))])
async def delete_user(user_id: str):
    return await userHandler.delete(user_id)
