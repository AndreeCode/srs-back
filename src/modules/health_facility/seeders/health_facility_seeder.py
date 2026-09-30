HEALTH_FACILITIES = [
    ("Belén", "Belén"),
    ("Barrios Altos", "Belén"),
    ("Huascahura", "Belén"),
    ("Santa Ana", "Belén"),
    ("Carmen Alto", "Carmen Alto"),
    ("Vista Alegre", "Carmen Alto"),
    ("Yanama", "Carmen Alto"),
    ("Chiara", "Chiara"),
    ("Allpachaca", "Chiara"),
    ("Chontaca", "Chontaca"),
    ("Acocro", "Chontaca"),
    ("Licenciados", "Licenciados"),
    ("Centro de Salud Nazareno", "Licenciados"),
    ("Mollepata", "Licenciados"),
    ("Muyurina", "Muyurina"),
    ("Pacaycasa", "Muyurina"),
    ("Simpapata", "Muyurina"),
]


async def seed_health_facilities(conn, region_ids: dict) -> dict[str, object]:
    await conn.executemany(
        "INSERT INTO health_facilities (name, region_id) VALUES ($1, $2) ON CONFLICT (name) DO NOTHING",
        [(name, region_ids[region]) for name, region in HEALTH_FACILITIES],
    )
    names = [name for name, _ in HEALTH_FACILITIES]
    rows = await conn.fetch("SELECT id, name FROM health_facilities WHERE name = ANY($1::text[])", names)
    print(f"establecimientos: {len(rows)}")
    return {row["name"]: row["id"] for row in rows}
