import struct
import zlib
from uuid import uuid4

from ....core.storage.file_storage import save_file


def sample_png() -> bytes:
    width, height = 64, 40
    raw = b"".join(b"\x00" + bytes((30, 120, 200)) * width for _ in range(height))

    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))

    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw))
        + chunk(b"IEND", b"")
    )


def sample_pdf(text: str) -> bytes:
    stream = f"BT /F1 14 Tf 60 780 Td ({text}) Tj ET".encode("latin-1")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out = b"%PDF-1.4\n"
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{number} 0 obj\n".encode() + body + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode()
    out += b"".join(f"{offset:010d} 00000 n \n".encode() for offset in offsets)
    out += f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    return out


EVIDENCES = [
    ("vacuna", "carnet_vacunacion.png", "image/png", ".png", sample_png),
    ("visita", "constancia_visita.pdf", "application/pdf", ".pdf", lambda: sample_pdf("Constancia de visita domiciliaria - EESS Vista Alegre")),
]


async def seed_claim_evidences(conn, claim_ids: dict) -> None:
    created = 0

    for key, original_name, mime_type, extension, build in EVIDENCES:
        claim_id = claim_ids[key]

        if await conn.fetchval(
            "SELECT 1 FROM claim_evidences WHERE claim_id = $1 AND original_name = $2", claim_id, original_name
        ):
            continue

        content = build()
        evidence_id = uuid4()
        storage_path = f"claims/{claim_id}/{evidence_id}{extension}"
        await save_file(storage_path, content)
        await conn.execute(
            """
            INSERT INTO claim_evidences (id, claim_id, original_name, storage_path, mime_type, size_bytes)
            VALUES ($1, $2, $3, $4, $5, $6)
            """,
            evidence_id,
            claim_id,
            original_name,
            storage_path,
            mime_type,
            len(content),
        )
        created += 1

    print(f"evidencias: {created} nuevas")
