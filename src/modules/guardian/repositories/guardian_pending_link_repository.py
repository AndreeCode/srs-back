from uuid import UUID

from ....core.db.connection import get_connection


async def get_pending_links() -> list[dict]:
    conn = await get_connection()

    try:
        rows = await conn.fetch(
            """
            SELECT 'sicna' AS source, cg.guardian_id, g.full_name AS guardian_name, g.dni AS guardian_dni,
                   cg.child_id::text AS child_key, c.first_names || ' ' || c.last_names AS child_name,
                   COALESCE(c.dni, c.padron_code) AS child_document, c.birth_date AS child_birth_date,
                   cg.relationship, cg.requested_at
            FROM child_guardian cg
            JOIN guardians g ON g.id = cg.guardian_id
            JOIN children c ON c.id = cg.child_id
            WHERE NOT cg.verified
            UNION ALL
            SELECT 'his' AS source, h.guardian_id, g.full_name, g.dni,
                   h.document_number, h.child_name, h.document_number, h.birth_date,
                   h.relationship, h.created_at
            FROM guardian_his_children h
            JOIN guardians g ON g.id = h.guardian_id
            WHERE NOT h.verified
            ORDER BY requested_at
            """
        )
        return [dict(row) for row in rows]

    finally:
        await conn.close()


async def approve_pending_link(source: str, guardian_id: UUID, child_key: str, verified_by: UUID) -> bool:
    conn = await get_connection()

    try:
        if source == "sicna":
            result = await conn.execute(
                """
                UPDATE child_guardian SET verified = TRUE, verified_by = $3, verified_at = NOW()
                WHERE guardian_id = $1 AND child_id = $2::uuid AND NOT verified
                """,
                guardian_id,
                child_key,
                verified_by,
            )
        else:
            result = await conn.execute(
                """
                UPDATE guardian_his_children SET verified = TRUE, verified_by = $3, verified_at = NOW()
                WHERE guardian_id = $1 AND document_number = $2 AND NOT verified
                """,
                guardian_id,
                child_key,
                verified_by,
            )
        return result.endswith(" 1")

    finally:
        await conn.close()


async def reject_pending_link(source: str, guardian_id: UUID, child_key: str) -> bool:
    conn = await get_connection()

    try:
        if source == "sicna":
            result = await conn.execute(
                "DELETE FROM child_guardian WHERE guardian_id = $1 AND child_id = $2::uuid AND NOT verified",
                guardian_id,
                child_key,
            )
        else:
            result = await conn.execute(
                "DELETE FROM guardian_his_children WHERE guardian_id = $1 AND document_number = $2 AND NOT verified",
                guardian_id,
                child_key,
            )
        return result.endswith(" 1")

    finally:
        await conn.close()
