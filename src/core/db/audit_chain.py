import asyncio
from datetime import datetime, timezone
from typing import Awaitable, Callable

from ..config.config import config
from ..logger.logger import logger
from .connection import get_connection

SEAL_INTERVAL_SECONDS = 60
VERIFY_EVERY_SEALS = 60
last_check: dict = {}


async def seal() -> int:
    conn = await get_connection()
    try:
        return await conn.fetchval("SELECT seal_audit_log($1)", config.audit_chain_key)
    finally:
        await conn.close()


async def verify() -> dict:
    conn = await get_connection()
    try:
        row = await conn.fetchrow("SELECT * FROM verify_audit_chain($1)", config.audit_chain_key)
    finally:
        await conn.close()
    return dict(row)


async def check_and_report() -> dict:
    await seal()
    result = await verify()
    last_check.clear()
    last_check.update(result, checked_at=datetime.now(timezone.utc))
    if result["ok"]:
        logger.info(
            f"Cadena de auditoria integra: {result['checked']} registros, ultimo seq {result['last_seq']} "
            f"hash {result['last_hash']}"
        )
    else:
        logger.error(
            f"ALERTA DE SEGURIDAD: cadena de auditoria rota en el registro {result['broken_seq']}: {result['reason']}"
        )
    return result


async def seal_loop(periodic_check: Callable[[], Awaitable[dict]] | None = None) -> None:
    rounds = 0
    while True:
        await asyncio.sleep(SEAL_INTERVAL_SECONDS)
        rounds += 1
        try:
            if rounds % VERIFY_EVERY_SEALS == 0:
                await (periodic_check or check_and_report)()
            else:
                await seal()
        except Exception as err:
            logger.error(f"No se pudo sellar o verificar la cadena de auditoria: {err}")
