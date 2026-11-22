from ....core.config.config import config
from ....core.security.password import generate_password, hash_password

USERS = [
    {
        "username": "admin",
        "password": "Admin123!",
        "role_name": "admin",
        "full_name": "Administrador General",
        "dni": "10000001",
        "phone": "900000001",
        "email": "admin@sicna.local",
    },
    {
        "username": "coordinador",
        "password": "Coord123!",
        "role_name": "health_staff",
        "full_name": "Coordinador de Salud",
        "dni": "10000002",
        "phone": "900000002",
        "email": "coordinador@sicna.local",
    },
    {
        "username": "usuario",
        "password": "Usuario123!",
        "role_name": "guardian",
        "full_name": "Usuario Apoderado",
        "dni": "10000003",
        "phone": "900000003",
        "email": "usuario@sicna.local",
    },
]


async def seed_users(conn, role_ids: dict) -> dict[str, object]:
    user_ids = {}

    for u in USERS:
        existing = await conn.fetchval("SELECT id FROM users WHERE username = $1", u["username"])

        if existing is not None:
            print(f"usuario ya existe: {u['username']} -> {existing}")
            user_ids[u["username"]] = existing
            continue

        password = generate_password() if config.is_production else u["password"]
        user_ids[u["username"]] = await conn.fetchval(
            """
            INSERT INTO users (username, password_hash, role_id, full_name, dni, phone, email,
                               terms_accepted, terms_version, terms_accepted_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7, TRUE, '1.0', NOW())
            RETURNING id
            """,
            u["username"],
            hash_password(password),
            role_ids[u["role_name"]],
            u["full_name"],
            u["dni"],
            u["phone"],
            u["email"],
        )
        print(f"usuario creado: {u['username']} / {password}")

    return user_ids
