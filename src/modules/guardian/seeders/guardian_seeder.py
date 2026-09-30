from ....core.security.password import hash_password

GUARDIAN_PASSWORD = "Padre123!"

GUARDIANS = [
    ("María Huamán Quispe", "40125896", "966123456", "maria.huaman@correo.pe", "usuario"),
    ("José Cárdenas Ramos", "41258963", "955789321", None, None),
    ("Carmen Palomino Soto", "40031676", "962004924", None, None),
    ("Rosa Llamocca Pariona", "40039595", "962006155", None, None),
    ("Julia Ccori Tineo", "40047514", "962007386", None, None),
    ("Elena Yupanqui Mendoza", "40055433", "962008617", None, None),
    ("Lucía Ayala Prado", "40063352", "962009848", None, None),
    ("Carla Barboza Janampa", "40071271", "962011079", None, None),
    ("Nancy Cisneros Ore", "40079190", "962012310", None, None),
    ("Pilar Vila Gutiérrez", "40087109", "962013541", None, None),
    ("Yolanda Sulca Ramos", "40095028", "962014772", None, None),
    ("Silvia Pillaca Díaz", "40102947", "962016003", None, None),
    ("Doris Chávez León", "40110866", "962017234", None, None),
    ("Gloria Quicaño Bautista", "40118785", "962018465", None, None),
    ("Irma Ñaupa Huayta", "40126704", "962019696", None, None),
    ("Flor Ccente Arango", "40134623", "962020927", None, None),
    ("Martha Palomino Rojas", "40142542", "962022158", None, None),
    ("Rocío Cuba Sánchez", "40150461", "962023389", None, None),
    ("Lourdes Taipe Mitma", "40158380", "962024620", None, None),
    ("Norma Condori Huillca", "40166299", "962025851", None, None),
    ("Betty Galindo Poma", "40174218", "962027082", None, None),
    ("Ana Rivera Loayza", "40182137", "962028313", None, None),
    ("Carmen Paucar Villa", "40190056", "962029544", None, None),
]


async def seed_guardians(conn, user_ids: dict) -> dict[str, object]:
    for full_name, dni, phone, email, username in GUARDIANS:
        user_id = user_ids.get(username) if username else None

        if user_id is not None and await conn.fetchval("SELECT 1 FROM guardians WHERE user_id = $1", user_id):
            user_id = None

        await conn.execute(
            """
            INSERT INTO guardians (full_name, dni, phone, email, user_id)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (dni) DO NOTHING
            """,
            full_name,
            dni,
            phone,
            email,
            user_id,
        )

    dnis = [guardian[1] for guardian in GUARDIANS]
    rows = await conn.fetch("SELECT id, dni FROM guardians WHERE dni = ANY($1::text[])", dnis)
    print(f"padres: {len(rows)}")
    return {row["dni"]: row["id"] for row in rows}


async def seed_guardian_accounts(conn, guardian_role_id) -> None:
    pending = await conn.fetch(
        """
        SELECT id, full_name, dni, phone, email FROM guardians
        WHERE user_id IS NULL AND active = true AND dni = ANY($1::text[])
        """,
        [guardian[1] for guardian in GUARDIANS],
    )
    password_hash = hash_password(GUARDIAN_PASSWORD) if pending else None
    created = 0

    for guardian in pending:
        user_id = await conn.fetchval("SELECT id FROM users WHERE username = $1", guardian["dni"])

        if user_id is None:
            user_id = await conn.fetchval(
                """
                INSERT INTO users (username, password_hash, role_id, full_name, dni, phone, email,
                                   terms_accepted, terms_version, terms_accepted_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, TRUE, '1.0', NOW())
                RETURNING id
                """,
                guardian["dni"],
                password_hash,
                guardian_role_id,
                guardian["full_name"],
                guardian["dni"],
                guardian["phone"],
                guardian["email"],
            )
            created += 1

        await conn.execute("UPDATE guardians SET user_id = $1 WHERE id = $2", user_id, guardian["id"])

    print(f"cuentas de padres: {created} nuevas (usuario = DNI, contraseña {GUARDIAN_PASSWORD})")
