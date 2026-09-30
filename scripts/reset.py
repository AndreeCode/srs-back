import argparse
import asyncio
import sys

import asyncpg

from scripts.migrate import connection_params


async def main(drop: bool, yes: bool, hint: bool = True) -> int:
    params = connection_params()
    try:
        conn = await asyncpg.connect(**params)
    except Exception as e:
        print(f"Could not connect: {e}")
        return 1

    db = await conn.fetchval("SELECT current_database()")
    tables = [
        r["tablename"]
        for r in await conn.fetch(
            "SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY 1"
        )
    ]

    print(f"Database: {db} at {params['host']}:{params['port']} (as {params['user']})")
    if drop:
        print("The WHOLE public schema will be DROPPED: tables, views, functions, types and data.")
        if hint:
            print("Then run: python -m scripts.migrate")
    else:
        print("ALL DATA will be DELETED (tables are kept):")
        for t in tables:
            n = await conn.fetchval(f'SELECT count(*) FROM "{t}"')
            print(f"  {t:<20} {n} rows")

    if not yes:
        if not sys.stdin.isatty():
            print("Confirmation required: run it in a terminal or pass --yes.")
            await conn.close()
            return 1
        if input(f"\nType the database name ({db}) to confirm: ").strip() != db:
            print("Cancelled. Nothing was changed.")
            await conn.close()
            return 1

    try:
        async with conn.transaction():
            if drop:
                await conn.execute("DROP SCHEMA public CASCADE")
                await conn.execute("CREATE SCHEMA public")
                await conn.execute("GRANT USAGE ON SCHEMA public TO PUBLIC")
            elif tables:
                await conn.execute(
                    "TRUNCATE " + ", ".join(f'"{t}"' for t in tables) + " RESTART IDENTITY CASCADE"
                )
    except asyncpg.exceptions.InsufficientPrivilegeError:
        print(f"User {params['user']} lacks privileges. Use the schema owner (DB_ADMIN_USER in .env).")
        await conn.close()
        return 1

    print("Schema dropped." if drop else "Data deleted.")
    await conn.close()
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Empties the database configured in .env.")
    parser.add_argument("--drop", action="store_true", help="drop the whole schema (not just the data)")
    parser.add_argument("--yes", action="store_true", help="do not ask for confirmation")
    args = parser.parse_args()
    sys.exit(asyncio.run(main(args.drop, args.yes)))
