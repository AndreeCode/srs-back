import json
from uuid import UUID

from ....core.db.connection import get_connection
from ....core.logger.logger import logger


async def log_auth_event(action: str, user_id: UUID | None, result: str, details: dict | None = None) -> None:
    try:
        conn = await get_connection()
        try:
            await conn.execute(
                "SELECT log_auth_event($1, $2, $3::result_type, $4::jsonb)",
                action,
                user_id,
                result,
                json.dumps(details) if details is not None else None,
            )
        finally:
            await conn.close()
    except Exception as err:
        logger.error(f"No se pudo registrar el evento {action}: {err}")
