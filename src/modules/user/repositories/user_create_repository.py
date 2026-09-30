from ....core.db.connection import get_connection
from ..domain.user_domain import User


async def create_user(user: User) -> User:
    conn = await get_connection()

    try:
        async with conn.transaction():
            row = await conn.fetchrow(
                """
                INSERT INTO users (
                    id, username, password_hash, role_id, full_name,
                    dni, phone, email,
                    terms_accepted, terms_version, terms_accepted_at,
                    active, blocked, blocked_reason
                )
                VALUES (
                    $1, $2, $3, $4, $5,
                    $6, $7, $8,
                    $9, $10, $11,
                    $12, $13, $14
                )
                RETURNING id, username, password_hash, role_id, full_name,
                          dni, phone, email,
                          terms_accepted, terms_version, terms_accepted_at,
                          active, blocked, blocked_reason,
                          created_at, updated_at
                """,
                user.id,
                user.username,
                user.password_hash,
                user.role_id,
                user.full_name,
                user.dni,
                user.phone,
                user.email,
                user.terms_accepted,
                user.terms_version,
                user.terms_accepted_at,
                user.active,
                user.blocked,
                user.blocked_reason,
            )

            if user.region_ids:
                await conn.executemany(
                    "INSERT INTO user_region (user_id, region_id) VALUES ($1, $2)",
                    [(row["id"], region_id) for region_id in user.region_ids],
                )

        created = User.from_row(row)
        created.region_ids = sorted(user.region_ids)
        return created

    finally:
        await conn.close()
