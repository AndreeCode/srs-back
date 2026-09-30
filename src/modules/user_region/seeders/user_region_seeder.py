USER_REGIONS = [
    ("coordinador", "Belén"),
    ("coordinador", "Carmen Alto"),
]


async def seed_user_regions(conn, user_ids: dict, region_ids: dict) -> None:
    await conn.executemany(
        "INSERT INTO user_region (user_id, region_id) VALUES ($1, $2) ON CONFLICT DO NOTHING",
        [(user_ids[username], region_ids[region]) for username, region in USER_REGIONS],
    )
    print(f"micro redes asignadas: {len(USER_REGIONS)}")
