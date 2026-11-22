import logging

import asyncpg

from src.core.config.config import config

from .audit_context import get_audit_context

logger = logging.getLogger(__name__)


async def get_connection():
    connection = await asyncpg.connect(
        host=config.dbhost,
        database=config.dbname,
        user=config.dbuser,
        password=config.dbpassword,
        ssl=config.db_sslmode,
        timeout=10,
        command_timeout=60,
    )

    audit_context = get_audit_context()

    if audit_context:
        await connection.execute(
            "SELECT set_config(key, value, false) FROM unnest($1::text[], $2::text[]) AS t(key, value)",
            list(audit_context.keys()),
            list(audit_context.values()),
        )

    logger.info("Base de datos conectada correctamente")
    return connection
