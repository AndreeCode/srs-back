import logging
from contextlib import asynccontextmanager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

from src.core.db.connection import get_connection
from src.core.http.exception_handlers import register_exception_handlers
from src.core.routes.routes import router as api_router
from src.core.security.auth_middleware import AuthMiddleware

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    conn = await get_connection()
    await conn.close()
    yield


app = FastAPI(lifespan=lifespan)

register_exception_handlers(app)
app.add_middleware(AuthMiddleware)
app.include_router(api_router, prefix="/api")


@app.get("/api")
def root():
    return {
        "message": "servidor corriendo correctamente",
        "status": 200,
    }
