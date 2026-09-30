from ....core.db.connection import get_connection
from ..domain.role_domain import Role


async def create_role(role: Role) -> Role:
    conn = await get_connection()

    try:
        async with conn.transaction():
            row = await conn.fetchrow(
                """
                INSERT INTO roles (id, name, is_active)
                VALUES ($1, $2, $3)
                RETURNING id, name, is_active
                """,
                role.id,
                role.name,
                role.is_active,
            )

            if role.permission_ids:
                await conn.executemany(
                    "INSERT INTO role_permission (role_id, permission_id) VALUES ($1, $2)",
                    [(row["id"], permission_id) for permission_id in role.permission_ids],
                )

        created = Role.from_row(row)
        created.permission_ids = sorted(role.permission_ids)
        return created

    finally:
        await conn.close()
