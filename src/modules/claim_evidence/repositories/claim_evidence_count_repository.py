from uuid import UUID

from ....core.db.connection import get_connection


async def count_claim_evidences(claim_id: UUID) -> int:
    conn = await get_connection()

    try:
        return await conn.fetchval("SELECT count(*) FROM claim_evidences WHERE claim_id = $1", claim_id)

    finally:
        await conn.close()
