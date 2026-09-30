from typing import Any

from fastapi.responses import JSONResponse


class SuccessResponse:
    def __init__(
        self,
        status: int,
        msg: str,
        data: Any = None,
    ):
        self.status = status
        self.msg = msg
        self.data = data


def success(
    status: int,
    msg: str,
    data: Any = None,
) -> JSONResponse:

    response = {
        "status": status,
        "msg": msg,
    }

    if data is not None:
        response["data"] = data

    return JSONResponse(
        status_code=status,
        content=response,
    )