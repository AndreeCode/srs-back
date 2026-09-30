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
    err: Exception,
) -> JSONResponse:

    logger.error(
        f"{msg}: {err}",
        exc_info=err,
    )

    response = ErrorResponse(
        status=status,
        msg=msg,
    )

    return JSONResponse(
        status_code=status,
        content=response.model_dump(),
    )