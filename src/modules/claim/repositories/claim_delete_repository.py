from uuid import UUID

from ....core.db.connection import get_connection


async def delete_claim(claim_id: UUID) -> list[str] | None:
    conn = await get_connection()

    try:
        async with conn.transaction():
            rows = await conn.fetch(
                "DELETE FROM claim_evidences WHERE claim_id = $1 RETURNING storage_path",
                claim_id,
            )
            result = await conn.execute("DELETE FROM claims WHERE id = $1", claim_id)

            if result.endswith(" 0"):
                return None

        return [row["storage_path"] for row in rows]

    finally:
        await conn.close()
