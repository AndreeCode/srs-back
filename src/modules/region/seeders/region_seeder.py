REGIONS = ["Belén", "Carmen Alto", "Chiara", "Chontaca", "Licenciados", "Muyurina"]


async def seed_regions(conn) -> dict[str, object]:
    await conn.executemany(
        "INSERT INTO regions (name) VALUES ($1) ON CONFLICT (name) DO NOTHING",
        [(name,) for name in REGIONS],
    )
    rows = await conn.fetch("SELECT id, name FROM regions WHERE name = ANY($1::text[])", REGIONS)
    print(f"micro redes: {len(rows)}")
    return {row["name"]: row["id"] for row in rows}
