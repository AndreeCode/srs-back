from datetime import date, datetime, time, timedelta, timezone

CLAIMS = [
    {
        "key": "vacuna",
        "padron": "PAD-0250317",
        "requester": "usuario",
        "requester_dni": "40125896",
        "facility": "Belén",
        "service": ("INMUNIZACIONES", "PENTA2"),
        "attention_days_ago": 40,
        "created_days_ago": 35,
        "message": "Mi hija recibió la vacuna Pentavalente 2.a dosis pero en el sistema aparece como pendiente.",
        "status": "in_review",
        "response": "Estamos verificando el registro con el EESS Belén.",
    },
    {
        "key": "hemoglobina",
        "padron": "PAD-0250334",
        "requester": "usuario",
        "requester_dni": "40125896",
        "facility": "Belén",
        "service": ("IAG_19", "HB_3"),
        "attention_days_ago": 10,
        "created_days_ago": 8,
        "message": "El dosaje de hemoglobina de mi hijo se hizo hace 10 días y no figura.",
        "status": "pending",
        "response": None,
    },
    {
        "key": "visita",
        "padron": "PAD-0250436",
        "requester": "admin",
        "requester_dni": "40063352",
        "facility": "Vista Alegre",
        "service": ("IAG_11", "VISITA_6M"),
        "attention_days_ago": 120,
        "created_days_ago": 58,
        "message": "La visita domiciliaria de 6 meses no está registrada.",
        "status": "resolved",
        "response": "Registro corregido por el EESS Vista Alegre.",
    },
]


def days_ago(days: int) -> datetime:
    return datetime.combine(date.today() - timedelta(days=days), time(9, 30), tzinfo=timezone.utc)


async def seed_claims(conn, children: dict, user_ids: dict, facility_ids: dict, service_ids: dict) -> dict[str, object]:
    claim_ids = {}

    for c in CLAIMS:
        child = children[c["padron"]]
        existing = await conn.fetchval(
            "SELECT id FROM claims WHERE child_id = $1 AND message = $2", child["id"], c["message"]
        )

        if existing is not None:
            claim_ids[c["key"]] = existing
            continue

        reviewed = c["status"] != "pending"
        claim_ids[c["key"]] = await conn.fetchval(
            """
            INSERT INTO claims (child_id, requester_user_id, requester_dni, child_dni, child_identifier,
                                health_facility_id, service_id, attention_date, message, status, response,
                                reviewed_by, reviewed_at, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10::claim_status, $11, $12, $13, $14, $14)
            RETURNING id
            """,
            child["id"],
            user_ids[c["requester"]],
            c["requester_dni"],
            child["dni"],
            c["padron"],
            facility_ids[c["facility"]],
            service_ids.get(c["service"]),
            date.today() - timedelta(days=c["attention_days_ago"]),
            c["message"],
            c["status"],
            c["response"],
            user_ids["admin"] if reviewed else None,
            days_ago(c["created_days_ago"] - 2) if reviewed else None,
            days_ago(c["created_days_ago"]),
        )

    print(f"reclamos: {len(claim_ids)}")
    return claim_ids
