import asyncio
import re

import pymssql

from src.core.config.config import config


class SqlServerUnavailableError(Exception):
    pass


class SqlServerReadOnlyError(Exception):
    pass


READ_ONLY = re.compile(r"^\s*(SELECT|WITH)\b", re.IGNORECASE)
WRITE_WORDS = re.compile(r"\b(INSERT|UPDATE|DELETE|MERGE|DROP|ALTER|CREATE|TRUNCATE|EXEC|EXECUTE|GRANT|REVOKE|DENY|BACKUP|RESTORE|INTO)\b", re.IGNORECASE)


def _fetch(query: str, params: tuple) -> list[dict]:
    try:
        conn = pymssql.connect(
            server=config.mssql_host,
            port=str(config.mssql_port),
            user=config.mssql_user,
            password=config.mssql_password,
            database=config.mssql_db,
            login_timeout=5,
            timeout=20,
            charset="UTF-8",
            as_dict=True,
            encryption=config.mssql_encryption,
        )
    except pymssql.Error as err:
        raise SqlServerUnavailableError("No se pudo conectar con HIS-MINSA (SQL Server)") from err

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    finally:
        conn.close()


async def sqlserver_fetch(query: str, params: tuple = ()) -> list[dict]:
    if not READ_ONLY.match(query) or WRITE_WORDS.search(query):
        raise SqlServerReadOnlyError("HIS-MINSA es de solo lectura: solo se permiten consultas SELECT")

    if not config.mssql_user:
        raise SqlServerUnavailableError("HIS-MINSA (SQL Server) no esta configurado: faltan MSSQL_USER / MSSQL_PASSWORD en el .env")

    return await asyncio.to_thread(_fetch, query, params)


def placeholders(count: int) -> str:
    return ", ".join(["%s"] * count)
