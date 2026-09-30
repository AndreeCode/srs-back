from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .error import error


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        details = []
        for err in exc.errors():
            field = ".".join(str(part) for part in err["loc"] if part != "body")
            details.append(f"{field}: {err['msg']}" if field else err["msg"])

        msg = "; ".join(details) if details else "Datos de la solicitud invalidos"
        return error(422, msg, exc)

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return error(exc.status_code, str(exc.detail), exc)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        return error(500, "Error interno del servidor", exc)
