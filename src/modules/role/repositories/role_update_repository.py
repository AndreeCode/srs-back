from ....core.db.connection import get_connection
from ..domain.role_domain import Role


async def update_role(role: Role) -> Role | None:
    conn = await get_connection()

    try:
        async with conn.transaction():
            row = await conn.fetchrow(
                """
                UPDATE roles
                SET name = $1, is_active = $2
                WHERE id = $3
                RETURNING id, name, is_active
                """,
                role.name,
                role.is_active,
                role.id,
            )

            if row is None:
                return None

            stored = {
                r["permission_id"]
                for r in await conn.fetch(
                    "SELECT permission_id FROM role_permission WHERE role_id = $1",
                    role.id,
                )
            }
            wanted = set(role.permission_ids)

            if stored - wanted:
                await conn.execute(
                    "DELETE FROM role_permission WHERE role_id = $1 AND permission_id = ANY($2::uuid[])",
                    role.id,
                    list(stored - wanted),
                )

            if wanted - stored:
                await conn.executemany(
                    "INSERT INTO role_permission (role_id, permission_id) VALUES ($1, $2)",
                    [(role.id, permission_id) for permission_id in wanted - stored],
                )

        updated = Role.from_row(row)
        updated.permission_ids = sorted(wanted)
        return updated

    finally:
        await conn.close()
