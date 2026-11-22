import asyncio
import getpass
import os
import sys
from pathlib import Path

import asyncpg
from dotenv import load_dotenv

SQL_DIR = Path(__file__).resolve().parent.parent / "src" / "core" / "db" / "sql"


def sql_files() -> list[Path]:
    files = [SQL_DIR / "init.sql"]
    migrations = SQL_DIR / "migrations"
    if migrations.is_dir():
        files += sorted(migrations.glob("*.sql"))
    return files


def connection_params() -> dict:
    load_dotenv(SQL_DIR.parents[3] / ".env")
    user = os.getenv("DB_ADMIN_USER") or os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_ADMIN_PASSWORD")
    if password is None and os.getenv("DB_ADMIN_USER") is None:
        password = os.getenv("DB_PASSWORD")
    if password is None and sys.stdin.isatty():
        password = getpass.getpass(f"Password for {user}: ") or None
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "ssl": os.getenv("DB_SSLMODE", "prefer").strip().lower(),
        "database": os.getenv("DB_NAME", "sicna"),
        "user": user,
        "password": password,
    }


async def main() -> int:
    params = connection_params()
    print(f"Connecting to {params['database']} at {params['host']}:{params['port']} as {params['user']}")
    try:
        conn = await asyncpg.connect(**params)
    except Exception as e:
        print(f"Could not connect: {e}")
        return 1

    exit_code = 0
    for path in sql_files():
        name = path.relative_to(SQL_DIR).as_posix()
        print(f"  → {name}: applying...")
        try:
            await conn.execute(path.read_text(encoding="utf-8"))
        except asyncpg.exceptions.InsufficientPrivilegeError:
            print(
                f"  ✗ {name}: user {params['user']} lacks privileges. Use the schema owner "
                "(DB_ADMIN_USER and DB_ADMIN_PASSWORD in .env)."
            )
            exit_code = 1
            break
        except Exception as e:
            first = str(e).splitlines()[0] if str(e) else type(e).__name__
            print(f"  ✗ {name}: {first}")
            print("    No change from this file was applied (the transaction was rolled back).")
            exit_code = 1
            break
        print(f"  ✓ {name}: applied")

    await conn.close()
    return exit_code


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
