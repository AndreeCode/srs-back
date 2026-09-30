CARE_PACKAGES = [
    ("INMUNIZACIONES", "Inmunizaciones 2026", 0, 1460, "Esquema de vacunación por hito de edad", False),
    ("IAG_08", "Neonatos", 0, 28, "CNV, atención inmediata, tamizaje y seguimiento del recién nacido", False),
    ("IAG_09", "Prematuros o bajo peso", 0, 730, "Culminación de suplementación con hierro", True),
    ("IAG_10", "Menores de 1 año", 0, 365, "CRED, vacunas, SOFE, hemoglobina y hierro", False),
    ("IAG_11", "Menores de 12 meses", 0, 365, "Visitas domiciliarias con consejería", False),
    ("IAG_13", "1 año", 365, 729, "CRED, inmunizaciones, hemoglobina y hierro", False),
    ("IAG_17", "2 años", 730, 1094, "CRED, hemoglobina, suplementación y antiparasitario", False),
    ("IAG_18", "2 años con crecimiento inadecuado", 730, 1094, "Seguimiento nutricional a 60 y 100 días", False),
    ("IAG_19", "3 años", 1095, 1459, "CRED, hemoglobina, suplementación y antiparasitario", False),
    ("IAG_20", "4 años", 1460, 1824, "CRED, hemoglobina, inmunizaciones, hierro y antiparasitario", False),
    ("IAG_25", "5 a 11 años", 1825, 4379, "CRED, hemoglobina y entregas sucesivas de SOFE", False),
    ("IAG_26", "Menores de 12 meses (ALI)", 0, 365, "Sesión demostrativa de preparación de alimentos ALI", False),
    ("AG_21", "6 meses a 6 años", 182, 2555, "Paquete odontológico PAQ I / PAQ II", False),
]


async def seed_care_packages(conn) -> dict[str, object]:
    await conn.executemany(
        """
        INSERT INTO care_packages (code, name, min_age_days, max_age_days, description, at_risk_newborn_only, sort_order)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        ON CONFLICT (code) DO NOTHING
        """,
        [(*package, order) for order, package in enumerate(CARE_PACKAGES, start=1)],
    )
    codes = [package[0] for package in CARE_PACKAGES]
    rows = await conn.fetch("SELECT id, code FROM care_packages WHERE code = ANY($1::text[])", codes)
    print(f"paquetes: {len(rows)}")
    return {row["code"]: row["id"] for row in rows}
