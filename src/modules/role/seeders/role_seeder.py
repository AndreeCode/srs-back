ROLES = ["admin", "health_staff", "guardian"]


async def seed_roles(conn) -> dict[str, object]:
    await conn.executemany(
        "INSERT INTO roles (name) VALUES ($1::role_type) ON CONFLICT (name) DO NOTHING",
        [(name,) for name in ROLES],
    )
    rows = await conn.fetch("SELECT id, name::text AS name FROM roles WHERE name::text = ANY($1::text[])", ROLES)
    role_ids = {row["name"]: row["id"] for row in rows}
    print(f"roles: {', '.join(ROLES)}")
    return role_ids
