from ....core.db.sqlserver import placeholders, sqlserver_fetch
from ..domain.his_domain import HisChild


async def find_his_children(document_numbers: list[str]) -> dict[str, HisChild]:
    if not document_numbers:
        return {}

    rows = await sqlserver_fetch(
        f"""
        SELECT p.Id_Paciente, p.Id_Tipo_Documento_Paciente, p.Numero_Documento_Paciente,
               p.Fecha_Nacimiento_Paciente, p.Id_Genero,
               e.Nombre_Establecimiento, e.MicroRed, e.Red
        FROM dbo.MAESTRO_PACIENTE p
        LEFT JOIN dbo.MAESTRO_HIS_ESTABLECIMIENTO e ON e.Id_Establecimiento = p.Id_Establecimiento
        WHERE p.Numero_Documento_Paciente IN ({placeholders(len(document_numbers))})
          AND p.Id_Tipo_Documento_Paciente IN (1, 6)
          AND p.Fecha_Nacimiento_Paciente IS NOT NULL
        ORDER BY p.Fecha_Modificacion DESC
        """,
        tuple(document_numbers),
    )

    grouped: dict[str, list[dict]] = {}
    for row in rows:
        grouped.setdefault(row["Numero_Documento_Paciente"].strip(), []).append(row)

    return {document: HisChild.from_rows(group) for document, group in grouped.items()}
