import logging
from contextlib import asynccontextmanager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

import asyncio

from src.core.config.config import config
from src.core.db import audit_chain
from src.core.db.connection import get_connection
from src.core.http.exception_handlers import register_exception_handlers
from src.core.logger.logger import logger
from src.core.storage.file_storage import secure_existing_files
from src.modules.audit_log.handlers.audit_log_verify_handler import verify_and_alert
from src.core.routes.routes import router as api_router
from src.core.security.auth_middleware import AuthMiddleware
from src.core.security.security_headers import SecurityHeadersMiddleware

from fastapi import FastAPI

config.ensure_valid()


@asynccontextmanager
async def lifespan(app: FastAPI):
    conn = await get_connection()
    await conn.close()
    try:
        secure_existing_files()
    except OSError as err:
        logger.error(f"No se pudieron ajustar los permisos de UPLOAD_DIR: {err}")
    try:
        await verify_and_alert()
    except Exception as err:
        logger.error(f"No se pudo verificar la cadena de auditoria: {err}")
    sealer = asyncio.create_task(audit_chain.seal_loop(verify_and_alert))
    yield
    sealer.cancel()


docs = not config.is_production
app = FastAPI(
    lifespan=lifespan,
    docs_url="/docs" if docs else None,
    redoc_url="/redoc" if docs else None,
    openapi_url="/openapi.json" if docs else None,
)

register_exception_handlers(app)
app.add_middleware(AuthMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.include_router(api_router, prefix="/api")


@app.get("/api")
def root():
    return {
        "message": "servidor corriendo correctamente",
        "status": 200,
    }
