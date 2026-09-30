from ....core.db.connection import get_connection
from ..domain.user_domain import User


async def update_user(user: User) -> User | None:
    conn = await get_connection()

    try:
        async with conn.transaction():
            row = await conn.fetchrow(
                """
                UPDATE users
                SET username = $1,
                    password_hash = $2,
                    role_id = $3,
                    full_name = $4,
                    dni = $5,
                    phone = $6,
                    email = $7,
                    terms_accepted = $8,
                    terms_version = $9,
                    terms_accepted_at = $10,
                    active = $11,
                    blocked = $12,
                    blocked_reason = $13
                WHERE id = $14
                RETURNING id, username, password_hash, role_id, full_name,
                          dni, phone, email,
                          terms_accepted, terms_version, terms_accepted_at,
                          active, blocked, blocked_reason,
                          created_at, updated_at
                """,
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
                user.id,
            )

            if row is None:
                return None

            stored = {
                r["region_id"]
                for r in await conn.fetch(
                    "SELECT region_id FROM user_region WHERE user_id = $1",
                    user.id,
                )
            }
            wanted = set(user.region_ids)

            if stored - wanted:
                await conn.execute(
                    "DELETE FROM user_region WHERE user_id = $1 AND region_id = ANY($2::uuid[])",
                    user.id,
                    list(stored - wanted),
                )

            if wanted - stored:
                await conn.executemany(
                    "INSERT INTO user_region (user_id, region_id) VALUES ($1, $2)",
                    [(user.id, region_id) for region_id in wanted - stored],
                )

        updated = User.from_row(row)
        updated.region_ids = sorted(wanted)
        return updated

    finally:
        await conn.close()
