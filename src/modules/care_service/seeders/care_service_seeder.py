VACCINES = [
    ("RN_BCG", "BCG al nacer", 0, 60),
    ("RN_HVB", "Hepatitis B al nacer", 0, 60),
    ("IPV1", "IPV 1.a dosis", 60, 150),
    ("PENTA1", "Penta 1.a dosis", 60, 150),
    ("ROTAVIRUS1", "Rotavirus 1.a dosis", 60, 180),
    ("NEUMO1", "Neumococo 1.a dosis", 60, 180),
    ("IPV2", "IPV 2.a dosis", 120, 300),
    ("PENTA2", "Penta 2.a dosis", 120, 300),
    ("ROTAVIRUS2", "Rotavirus 2.a dosis", 120, 240),
    ("NEUMO2", "Neumococo 2.a dosis", 120, 300),
    ("IPV3", "IPV 3.a dosis", 180, 365),
    ("PENTA3", "Penta 3.a dosis", 180, 365),
    ("INFLUENZA", "Influenza pediátrica", 180, 730),
    ("SPR1", "SPR 1.a dosis", 365, 540),
    ("DPT1", "DPT 1.er refuerzo", 365, 730),
]

CARE_SERVICES = {
    "INMUNIZACIONES": [("DIRECTO", VACCINES)],
    "IAG_08": [
        ("CNV EN LINEA", [
            ("CNV_LIGA", "Liga / corte CNV", 0, 28),
            ("CNV_LACTANCIA", "Cumple lactancia precoz CNV", 0, 28),
            ("CNV", "Cumple CNV", 0, 28),
        ]),
        ("ATENCION INMEDIATA DEL RECIEN NACIDO", [
            ("BCG", "BCG", 0, 28),
            ("HVB", "Hepatitis B", 0, 28),
            ("CPP", "Contacto piel a piel", 0, 28),
            ("LME", "Lactancia materna exclusiva primera hora", 0, 28),
        ]),
        ("TAMIZAJE NEONATAL", [("TAMIZAJE", "Tamizaje neonatal", 0, 28)]),
        ("CONTROL CRED RN", [
            ("CRED_RN_1", "CRED N.° 01", 0, 28),
            ("CRED_RN_2", "CRED N.° 02", 0, 28),
            ("CRED_RN_3", "CRED N.° 03", 0, 28),
            ("CRED_RN_4", "CRED N.° 04", 0, 28),
        ]),
        ("VISITA DOMICILIARIA", [
            ("VISITA_ANAMNESIS", "Anamnesis y examen físico", 0, 28),
            ("VISITA_FAMILIAR", "Visita familiar", 0, 28),
            ("VISITA_CUIDADO", "Cuidado neonatal", 0, 28),
            ("VISITA_LACTANCIA", "Consejería de lactancia materna", 0, 28),
            ("VISITA_CORDON", "Cuidado del cordón umbilical", 0, 28),
            ("VISITA_ALARMA", "Signos de alarma", 0, 28),
            ("VISITA_HIGIENE", "Higiene del recién nacido", 0, 28),
        ]),
    ],
    "IAG_09": [("DIRECTO", [
        ("HIERRO_PREMATURO", "Culminación de suplementación con hierro", 0, 730),
        ("HB_PREMATURO", "Dosaje de hemoglobina", 0, 730),
    ])],
    "IAG_10": [
        ("CRED RECIEN NACIDO", [("CRED_RN", "CRED recién nacido", 0, 365)]),
        ("CRED DE 1 A 11 MESES", [("CRED_MENOR", "CRED de 1 a 11 meses", 0, 365)]),
        ("VACUNAS", [
            ("NEUMO", "Neumococo", 60, 365),
            ("ROTAVIRUS", "Rotavirus", 60, 365),
            ("IPV", "IPV", 60, 365),
            ("PENTA", "Pentavalente", 60, 365),
        ]),
        ("ENTREGA DE SOFE", [("SOFE", "Entrega de sulfato ferroso", 60, 365)]),
        ("DOSAJE DE HEMOGLOBINA", [("HB", "Dosaje de hemoglobina", 180, 365)]),
        ("SUPLEMENTACION CON HIERRO", [("HIERRO", "Suplementación con hierro", 60, 365)]),
    ],
    "IAG_11": [
        ("VISITA DOMICILIARIA RECIEN NACIDO", [("VISITA_RN", "Visita RN: lactancia, cordón y signos de alarma", 0, 60)]),
        ("VISITA 04 MESES", [("VISITA_4M", "Visita domiciliaria 4 meses", 90, 150)]),
        ("VISITA 06 MESES", [("VISITA_6M", "Visita domiciliaria 6 meses", 150, 240)]),
        ("VISITA DOMICILIARIA 08 MESES", [("VISITA_8M", "Visita domiciliaria 8 meses", 210, 300)]),
        ("VISITA DOMICILIARIA 09 MESES", [("VISITA_9M", "Visita domiciliaria 9 meses", 240, 365)]),
    ],
    "IAG_13": [
        ("CRED 01 AÑO", [("CRED_1", "CRED 01 año", 365, 729)]),
        ("INMUNIZACIONES", [("INMUNIZACION_1", "Inmunizaciones del año", 365, 729)]),
        ("DOSAJE DE HEMOGLOBINA", [("HB_1", "Dosaje de hemoglobina", 365, 729)]),
        ("SUPLEMENTACION CON HIERRO", [("HIERRO_1", "Suplementación con hierro", 365, 729)]),
    ],
    "IAG_17": [
        ("CRED 02 AÑOS", [("CRED_2", "CRED 02 años", 730, 1094)]),
        ("DOSAJE DE HEMOGLOBINA", [("HB_2", "Dosaje de hemoglobina", 730, 1094)]),
        ("SUPLEMENTACION - ESQUEMA 2 AÑOS", [("HIERRO_2", "Suplementación esquema 2 años", 730, 1094)]),
        ("PROFILAXIS ANTIPARASITARIA", [("ANTIPARASITARIO_2", "Profilaxis antiparasitaria", 730, 1094)]),
    ],
    "IAG_18": [("DIRECTO", [
        ("NUTRICION_60", "Seguimiento nutricional a 60 días", 730, 1094),
        ("NUTRICION_100", "Seguimiento nutricional a 100 días", 730, 1094),
    ])],
    "IAG_19": [
        ("CRED 03 AÑOS", [("CRED_3", "CRED 03 años", 1095, 1459)]),
        ("DOSAJE DE HEMOGLOBINA", [("HB_3", "Dosaje de hemoglobina", 1095, 1459)]),
        ("SUPLEMENTACION - ESQUEMA 03 AÑOS", [("HIERRO_3", "Suplementación esquema 3 años", 1095, 1459)]),
        ("PROFILAXIS ANTIPARASITARIA", [("ANTIPARASITARIO_3", "Profilaxis antiparasitaria", 1095, 1459)]),
    ],
    "IAG_20": [
        ("CRED 04 AÑOS", [("CRED_4", "CRED 04 años", 1460, 1824)]),
        ("DOSAJE DE HEMOGLOBINA", [("HB_4", "Dosaje de hemoglobina", 1460, 1824)]),
        ("INMUNIZACIONES", [("INMUNIZACION_4", "Inmunizaciones de 4 años", 1460, 1824)]),
        ("SUPLEMENTACION - ESQUEMA 04 AÑOS", [("HIERRO_4", "Suplementación esquema 4 años", 1460, 1824)]),
        ("PROFILAXIS ANTIPARASITARIA", [("ANTIPARASITARIO_4", "Profilaxis antiparasitaria", 1460, 1824)]),
    ],
    "IAG_25": [("NIÑAS/NIÑOS DE 5 A 11 AÑOS", [
        ("CRED_5_11", "CRED 5 a 11 años", 1825, 4379),
        ("HB_5_11", "Dosaje de hemoglobina", 1825, 4379),
        ("SOFE1", "1.a entrega sucesiva de SOFE", 1825, 4379),
        ("SOFE2", "2.a entrega sucesiva de SOFE", 1825, 4379),
        ("SOFE3", "3.a entrega sucesiva de SOFE", 1825, 4379),
        ("SOFE_TA", "Entrega adicional de SOFE", 1825, 4379),
        ("ANTIPARASITARIO_5_11", "Profilaxis antiparasitaria", 1825, 4379),
        ("VPH", "Vacuna VPH", 1825, 4379),
    ])],
    "IAG_26": [("RECIBE SESIONES DEMOSTRATIVA EN ALI", [
        ("ALI", "Sesión demostrativa de preparación de alimentos ALI", 0, 365),
        ("ALI_GOBIERNO_LOCAL", "Sesión promovida por gobierno local", 0, 365),
    ])],
    "AG_21": [("CARTERA ODONTOLÓGICA", [
        ("EVAL_ORAL", "Evaluación oral", 182, 2555),
        ("PAQ_ODONT_1", "Paquete odontológico preventivo I", 182, 2555),
        ("PAQ_ODONT_2", "Paquete odontológico preventivo II", 182, 2555),
    ])],
}


async def seed_care_services(conn, package_ids: dict) -> dict[tuple[str, str], object]:
    rows = []

    for package_code, groups in CARE_SERVICES.items():
        sort_order = 1
        for group_order, (group_name, services) in enumerate(groups, start=1):
            for code, name, min_age, max_age in services:
                rows.append((package_ids[package_code], code, name, group_name, group_order, sort_order, min_age, max_age))
                sort_order += 1

    await conn.executemany(
        """
        INSERT INTO care_services (package_id, code, name, group_name, group_order, sort_order, min_age_days, max_age_days)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        ON CONFLICT (package_id, code) DO NOTHING
        """,
        rows,
    )

    saved = await conn.fetch(
        """
        SELECT s.id, s.code, p.code AS package_code
        FROM care_services s JOIN care_packages p ON p.id = s.package_id
        WHERE p.code = ANY($1::text[])
        """,
        list(CARE_SERVICES),
    )
    print(f"prestaciones: {len(saved)}")
    return {(row["package_code"], row["code"]): row["id"] for row in saved}
