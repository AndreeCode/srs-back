from ....core.db.sqlserver import placeholders, sqlserver_fetch
from ..domain.his_domain import HisAttention


async def get_his_attentions(patient_ids: list[str]) -> list[HisAttention]:
    if not patient_ids:
        return []

    rows = await sqlserver_fetch(
        f"""
        SELECT n.Id_Paciente, n.Fecha_Atencion, n.Codigo_Item, n.Id_Dosis, n.Valor_Lab,
               n.Lote, n.Num_Pag, n.Num_Reg, n.Peso, n.Talla, n.Hemoglobina,
               (SELECT TOP 1 c.Descripcion_Item FROM dbo.MAESTRO_HIS_CIE_CPMS c WHERE c.Codigo_Item = n.Codigo_Item) AS Descripcion_Item,
               (SELECT TOP 1 d.desc_dosis FROM dbo.MAESTRO_HIS_DOSIS d WHERE d.id_dosis = n.Id_Dosis) AS Dosis,
               (SELECT TOP 1 e.Nombre_Establecimiento FROM dbo.MAESTRO_HIS_ESTABLECIMIENTO e WHERE e.Id_Establecimiento = n.Id_Establecimiento) AS Nombre_Establecimiento
        FROM dbo.NOMINAL_TRAMA_NUEVO n
        WHERE n.Id_Paciente IN ({placeholders(len(patient_ids))})
        ORDER BY n.Fecha_Atencion, n.Id_Correlativo_Item
        """,
        tuple(patient_ids),
    )

    return [HisAttention.from_row(row) for row in rows if row["Fecha_Atencion"] is not None]
