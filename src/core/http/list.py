from typing import Any

from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ListResponse(BaseModel):
    status: int
    msg: str
    data: Any | None = None
    meta: Any | None = None


def list_response(
    status: int,
    msg: str,
    data: Any = None,
    meta: Any = None,
) -> JSONResponse:

    response = ListResponse(
        status=status,
        msg=msg,
        data=data,
        meta=meta,
    )

    return JSONResponse(
        status_code=status,
        content=response.model_dump(exclude_none=True),
    )