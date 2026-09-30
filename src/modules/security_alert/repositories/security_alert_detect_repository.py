import json
from uuid import UUID

from ....core.db.connection import get_connection


async def find_shared_devices(min_accounts: int, days: int, device_hash: str | None) -> list[dict]:
    conn = await get_connection()

    try:
        rows = await conn.fetch(
            """
            SELECT d.device_hash,
                   count(DISTINCT d.user_id) AS total,
                   jsonb_agg(jsonb_build_object(
                       'device_id', d.id, 'user_id', u.id, 'username', u.username, 'full_name', u.full_name,
                       'user_blocked', u.blocked, 'trusted', d.trusted, 'user_agent', d.user_agent,
                       'last_seen_at', d.last_seen_at
                   ) ORDER BY d.last_seen_at DESC) AS items
            FROM devices d
            JOIN users u ON u.id = d.user_id
            WHERE d.last_seen_at >= NOW() - make_interval(days => $2)
              AND ($3::text IS NULL OR d.device_hash = $3)
            GROUP BY d.device_hash
            HAVING count(DISTINCT d.user_id) >= $1
            """,
            min_accounts,
            days,
            device_hash,
        )

        return [
            {"subject": row["device_hash"], "device_hash": row["device_hash"], "user_id": None,
             "detail": {"total": row["total"], "items": json.loads(row["items"])}}
            for row in rows
        ]

    finally:
        await conn.close()


async def find_many_devices(min_devices: int, days: int, user_id: UUID | None) -> list[dict]:
    conn = await get_connection()

    try:
        rows = await conn.fetch(
            """
            SELECT u.id AS user_id, u.username, u.full_name, u.blocked,
                   count(*) AS total,
                   jsonb_agg(jsonb_build_object(
                       'device_id', d.id, 'browser', left(d.device_hash, 10), 'trusted', d.trusted,
                       'user_agent', d.user_agent, 'last_seen_at', d.last_seen_at
                   ) ORDER BY d.last_seen_at DESC) AS items
            FROM devices d
            JOIN users u ON u.id = d.user_id
            WHERE d.last_seen_at >= NOW() - make_interval(days => $2)
              AND ($3::uuid IS NULL OR d.user_id = $3)
            GROUP BY u.id, u.username, u.full_name, u.blocked
            HAVING count(*) >= $1
            """,
            min_devices,
            days,
            user_id,
        )

        return [
            {"subject": str(row["user_id"]), "device_hash": None, "user_id": row["user_id"],
             "detail": {"total": row["total"], "username": row["username"], "full_name": row["full_name"],
                        "user_blocked": row["blocked"], "items": json.loads(row["items"])}}
            for row in rows
        ]

    finally:
        await conn.close()


async def save_alert(kind: str, found: dict, quiet_days: int) -> bool:
    conn = await get_connection()

    try:
        async with conn.transaction():
            recently_closed = await conn.fetchval(
                """
                SELECT 1 FROM security_alerts
                WHERE kind = $1 AND subject = $2 AND status <> 'open'
                  AND resolved_at >= NOW() - make_interval(days => $3)
                  AND (detail->>'total')::int >= $4
                LIMIT 1
                """,
                kind,
                found["subject"],
                quiet_days,
                found["detail"]["total"],
            )

            if recently_closed:
                return False

            created = await conn.fetchval(
                """
                INSERT INTO security_alerts (kind, subject, user_id, device_hash, detail)
                VALUES ($1, $2, $3, $4, $5::jsonb)
                ON CONFLICT (kind, subject) WHERE status = 'open'
                DO UPDATE SET detail = EXCLUDED.detail
                RETURNING (xmax = 0)
                """,
                kind,
                found["subject"],
                found["user_id"],
                found["device_hash"],
                json.dumps(found["detail"]),
            )

            return bool(created)

    finally:
        await conn.close()
