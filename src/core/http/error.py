from typing import Any

from fastapi.responses import JSONResponse
from pydantic import BaseModel

from ..logger.logger import logger


class ErrorResponse(BaseModel):
    status: int
    msg: str


def error(
    status: int,
    msg: str,
    err: Exception | None = None,
) -> JSONResponse:

    if status >= 500:
        logger.error(f"{status} {msg}: {err}", exc_info=err)
    else:
        logger.warning(f"{status} {msg}: {type(err).__name__}: {err}" if err else f"{status} {msg}")

    response = ErrorResponse(
        status=status,
        msg=msg,
    )

    return JSONResponse(
        status_code=status,
        content=response.model_dump(),
    )